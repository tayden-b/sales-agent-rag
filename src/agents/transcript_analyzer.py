"""
Agent 1: Transcript Analyzer
Extracts structured intelligence from raw call transcripts.
No tools needed — pure LLM analysis.
"""

from crewai import Agent

from src.config import LLM_MODEL


def create_transcript_analyzer() -> Agent:
    """Create the Transcript Analyzer agent."""
    return Agent(
        role="Senior Sales Call Analyst",
        goal=(
            "Extract structured, actionable intelligence from raw sales call transcripts. "
            "Identify the account stage, products discussed, technical concerns, pain points, "
            "competitor mentions, action items, and overall sentiment."
        ),
        backstory=(
            "You are a seasoned sales analyst with 15 years of experience in enterprise software sales, "
            "specializing in infrastructure and DevOps tools. You have an exceptional ability to read "
            "between the lines of customer conversations — picking up on subtle buying signals, "
            "hidden objections, and unstated needs. You understand the HashiCorp product suite deeply "
            "(Vault, Terraform, Consul) and can quickly identify where a deal stands in the sales cycle."
        ),
        llm=LLM_MODEL,
        verbose=True,
        allow_delegation=False,
    )
