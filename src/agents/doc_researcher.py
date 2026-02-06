"""
Agent 2: Documentation Researcher
Searches HashiCorp docs for relevant information about each technical concern.
"""

from crewai import Agent

from src.config import LLM_MODEL
from src.tools.doc_search import search_hashicorp_docs


def create_doc_researcher() -> Agent:
    """Create the Documentation Researcher agent."""
    return Agent(
        role="HashiCorp Technical Documentation Specialist",
        goal=(
            "Find the most relevant HashiCorp documentation for each technical concern "
            "raised in the customer call. Provide specific documentation references with "
            "excerpts and actionable recommendations for addressing each concern."
        ),
        backstory=(
            "You are a HashiCorp solutions architect with deep expertise in Vault, Terraform, "
            "and Consul. You know the documentation inside and out and can quickly find the "
            "exact guide, reference page, or tutorial that addresses a customer's specific "
            "technical question. You translate complex documentation into clear, concise "
            "recommendations that sales engineers can share with customers."
        ),
        llm=LLM_MODEL,
        tools=[search_hashicorp_docs],
        verbose=True,
        allow_delegation=False,
    )
