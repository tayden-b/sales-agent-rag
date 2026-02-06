"""
Agent 5: Knowledge Base Updater
Stores the processed transcript and analysis in the vector database.
"""

from crewai import Agent

from src.config import LLM_MODEL
from src.tools.vector_store import store_transcript_in_kb


def create_knowledge_updater() -> Agent:
    """Create the Knowledge Base Updater agent."""
    return Agent(
        role="Knowledge Management Specialist",
        goal=(
            "Store the current call transcript and its analysis in the knowledge base "
            "so it can be found and referenced in future call analyses. Ensure the transcript "
            "is tagged with accurate metadata for effective retrieval."
        ),
        backstory=(
            "You are a meticulous knowledge manager who understands that a well-organized "
            "knowledge base is only as good as its metadata. You ensure every transcript is "
            "stored with accurate account name, date, stage, products, and sentiment tags "
            "so future searches return the most relevant results."
        ),
        llm=LLM_MODEL,
        tools=[store_transcript_in_kb],
        verbose=True,
        allow_delegation=False,
    )
