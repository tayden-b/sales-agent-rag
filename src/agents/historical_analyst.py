"""
Agent 3: Historical Context Analyst
Searches past call transcripts for similar situations and patterns.
"""

from crewai import Agent

from src.config import LLM_MODEL
from src.tools.transcript_search import search_past_transcripts


def create_historical_analyst() -> Agent:
    """Create the Historical Context Analyst agent."""
    return Agent(
        role="Sales Intelligence Analyst",
        goal=(
            "Search past call transcripts to find similar deals, recurring patterns, "
            "and strategies that worked before. Provide historical context that helps "
            "the team make better decisions about the current deal."
        ),
        backstory=(
            "You are a sales intelligence specialist who excels at pattern recognition "
            "across customer interactions. You have a talent for connecting dots between "
            "different deals — noticing when a current customer's concerns mirror a past "
            "successful (or unsuccessful) engagement. Your historical insights help the team "
            "avoid repeating mistakes and replicate winning strategies. When no historical "
            "data is available, you clearly state that and suggest what to look for as the "
            "knowledge base grows."
        ),
        llm=LLM_MODEL,
        tools=[search_past_transcripts],
        verbose=True,
        allow_delegation=False,
    )
