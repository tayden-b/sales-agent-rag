"""
Agent 4: Email Composer
Synthesizes all analysis into a clear, actionable email.
No tools needed — pure LLM synthesis.
"""

from crewai import Agent

from src.config import LLM_MODEL


def create_email_composer() -> Agent:
    """Create the Email Composer agent."""
    return Agent(
        role="Executive Communications Specialist",
        goal=(
            "Synthesize the transcript analysis, documentation research, and historical context "
            "into a well-structured, professional email that a sales team can immediately act on. "
            "The email should be clear, concise, and prioritize actionable information."
        ),
        backstory=(
            "You are an expert at distilling complex technical and business information into "
            "clear, scannable communications for busy executives and sales teams. You know that "
            "the best internal emails lead with the most important information, use bullet points "
            "and headers for scannability, and end with clear next steps. You never pad with filler — "
            "every sentence earns its place."
        ),
        llm=LLM_MODEL,
        verbose=True,
        allow_delegation=False,
    )
