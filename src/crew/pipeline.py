"""
CrewAI crew definition and task orchestration.

Defines the 5-agent sequential pipeline:
  1. Transcript Analyzer → structured extraction
  2. Documentation Researcher → relevant docs for each concern
  3. Historical Context Analyst → similar past calls
  4. Email Composer → formatted email content
  5. Knowledge Base Updater → store transcript for future use
"""

import logging

from crewai import Agent, Crew, Task, Process

from src.agents.transcript_analyzer import create_transcript_analyzer
from src.agents.doc_researcher import create_doc_researcher
from src.agents.historical_analyst import create_historical_analyst
from src.agents.email_composer import create_email_composer
from src.agents.knowledge_updater import create_knowledge_updater
from src.schemas import TranscriptAnalysis

logger = logging.getLogger(__name__)


def build_analyze_task(transcript: str) -> tuple[Agent, Task]:
    """Build the Transcript Analyzer agent and its analyze task.

    Shared by the full pipeline and the standalone analyzer the extraction eval
    uses, so the prompt and the output_pydantic boundary stay identical between
    a real run and what the eval scores.
    """
    analyzer = create_transcript_analyzer()
    analyze_task = Task(
        description=f"""Analyze the following sales call transcript and extract structured information.

TRANSCRIPT:
---
{transcript}
---

Extract the following as a JSON object:
- account_name: The customer/company name
- call_date: Date of the call (or "unknown" if not mentioned)
- account_stage: One of: Discovery, Evaluation, POC, Negotiation, Renewal, Expansion
- products_discussed: List of HashiCorp products mentioned (Vault, Terraform, Consul, etc.)
- technical_concerns: List of objects with "concern" (brief description), "context_quote" (what the customer said), and "severity" (high/medium/low)
- pain_points: List of customer pain points or challenges mentioned
- competitors_mentioned: List of any competitor products or companies mentioned
- action_items: List of objects with "action" (what needs to be done), "owner" (who should do it), and "priority" (high/medium/low)
- sentiment: One of: Positive, Neutral, Cautious, Negative
- key_quotes: List of 2-3 notable customer statements

Return ONLY valid JSON. No additional text.""",
        expected_output="A JSON object with account_name, call_date, account_stage, products_discussed, technical_concerns, pain_points, competitors_mentioned, action_items, sentiment, and key_quotes.",
        agent=analyzer,
        output_pydantic=TranscriptAnalysis,
    )
    return analyzer, analyze_task


def run_analyzer(transcript: str) -> TranscriptAnalysis:
    """Run only the Transcript Analyzer and return its validated extraction.

    The extraction eval calls this to score analysis quality without running the
    downstream research/email agents.
    """
    analyzer, analyze_task = build_analyze_task(transcript)
    crew = Crew(
        agents=[analyzer],
        tasks=[analyze_task],
        process=Process.sequential,
        verbose=False,
    )
    crew.kickoff()
    parsed = analyze_task.output.pydantic if analyze_task.output else None
    if not isinstance(parsed, TranscriptAnalysis):
        raise ValueError("Analyzer output did not validate against TranscriptAnalysis")
    return parsed


def run_pipeline(transcript: str) -> dict:
    """
    Run the full analysis pipeline on a call transcript.

    Args:
        transcript: The raw call transcript text

    Returns:
        dict with keys:
          - email_subject: str
          - email_body: str (markdown formatted)
          - analysis: str (raw analysis from agent 1)
          - success: bool
    """
    logger.info("Creating agents...")
    analyzer, analyze_task = build_analyze_task(transcript)
    doc_researcher = create_doc_researcher()
    historian = create_historical_analyst()
    composer = create_email_composer()
    updater = create_knowledge_updater()

    # --- Task 2: Research documentation ---
    doc_research_task = Task(
        description="""Using the transcript analysis from the previous task, search the HashiCorp
documentation for relevant information about each technical concern identified.

For each technical concern:
1. Search the documentation using the concern description and related product
2. Find the most relevant documentation sections
3. Provide a clear recommendation for addressing the concern

Return a JSON object with a "concerns" array, where each entry has:
- concern: The technical concern description
- relevant_docs: List of relevant documentation findings (content, product, source_file)
- recommendation: A specific, actionable recommendation

If no documentation is found for a concern, still include it with an empty relevant_docs list
and a general recommendation.""",
        expected_output="A JSON object with a 'concerns' array mapping each technical concern to relevant documentation and recommendations.",
        agent=doc_researcher,
        context=[analyze_task],
    )

    # --- Task 3: Search historical context ---
    historical_task = Task(
        description="""Using the transcript analysis from the first task, search past call transcripts
for similar situations, patterns, and useful context.

Search for:
1. Calls with similar technical concerns
2. Calls at the same account stage with the same products
3. Calls with similar sentiment or pain points

Return a JSON object with:
- similar_calls: List of similar past calls found (account_name, call_date, similarity_reason, relevance)
- patterns: List of observed patterns across similar situations
- suggestions: List of strategies or approaches that worked well in similar situations

If no past transcripts are available (empty knowledge base), return the JSON with empty lists
and a note that the knowledge base will improve as more calls are processed.""",
        expected_output="A JSON object with similar_calls, patterns, and suggestions from historical data.",
        agent=historian,
        context=[analyze_task],
    )

    # --- Task 4: Compose the email ---
    compose_task = Task(
        description="""Using ALL the information gathered by the previous agents (transcript analysis,
documentation research, and historical context), compose a professional email summary.

The email MUST follow this EXACT structure in markdown format:

## Executive Summary
- [3-4 bullet points with the most important takeaways from the call]

## Technical Concerns & Documentation

### Concern 1: [Brief title]
**Context**: [What the customer said or asked]
- **Documentation**: [Relevant doc reference or link]
- **Recommendation**: [How to address this concern]

[Repeat for each concern]

## Recommended Next Steps
1. [Highest priority action] - Owner: [Who should do this]
2. [Next priority action] - Owner: [Who]
3. [Additional actions as needed]

## Resources to Share with Customer
- [Resource 1]: [Why this is helpful]
- [Resource 2]: [Why this is helpful]

## Internal Notes
- **Deal Health**: [Healthy / At-Risk / Needs Attention]
- **Key Risks**: [Any blockers or concerns]
- **Historical Context**: [Similar deals and patterns, or "First call in knowledge base"]
- **Strategic Notes**: [High-level observations and recommendations]

Write concisely. Every sentence should be actionable or informative. No filler.""",
        expected_output="A complete email body in markdown format following the specified structure with all sections filled in.",
        agent=composer,
        context=[analyze_task, doc_research_task, historical_task],
    )

    # --- Task 5: Store in knowledge base ---
    kb_update_task = Task(
        description="""Store the current call transcript in the knowledge base for future reference.

Using the transcript analysis from the first task, call the "Store Transcript in Knowledge Base"
tool with:
- transcript_text: The original transcript text (from the first task's input)
- account_name: From the analysis
- call_date: From the analysis
- account_stage: From the analysis
- products: Comma-separated list of products discussed
- sentiment: From the analysis
- summary: A brief 2-3 sentence summary of the call

Confirm that the transcript was stored successfully.""",
        expected_output="Confirmation that the transcript was stored in the knowledge base with its document ID.",
        agent=updater,
        context=[analyze_task],
    )

    # --- Assemble and run the crew ---
    logger.info("Assembling crew and starting pipeline...")
    crew = Crew(
        agents=[analyzer, doc_researcher, historian, composer, updater],
        tasks=[analyze_task, doc_research_task, historical_task, compose_task, kb_update_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # Extract results — the compose_task output is what we need for the email
    # CrewAI returns the final task's output by default, but we want the email content
    email_body = compose_task.output.raw if compose_task.output else ""
    analysis = analyze_task.output.raw if analyze_task.output else ""

    # Pull account info for the subject line off the validated model. With
    # output_pydantic set, CrewAI has already coerced the analyzer's JSON into a
    # TranscriptAnalysis (or failed the task), so no hand-rolled JSON parsing.
    account_name = "Customer"
    call_date = "Unknown Date"
    parsed = analyze_task.output.pydantic if analyze_task.output else None
    if isinstance(parsed, TranscriptAnalysis):
        account_name = parsed.account_name
        call_date = parsed.call_date
    else:
        logger.warning("Analyzer output did not validate; using defaults for the subject line.")

    logger.info("Pipeline complete.")

    return {
        "email_subject": f"Call Summary: {account_name} - {call_date}",
        "email_body": email_body,
        "analysis": analysis,
        "success": True,
    }
