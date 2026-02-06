"""
CrewAI tool for storing transcripts in the vector database.
Used by the Knowledge Base Updater agent.
"""

import json
from crewai.tools import tool

from src.rag.search import store_transcript


@tool("Store Transcript in Knowledge Base")
def store_transcript_in_kb(
    transcript_text: str,
    account_name: str,
    call_date: str,
    account_stage: str,
    products: str,
    sentiment: str,
    summary: str,
) -> str:
    """Store a processed call transcript in the knowledge base for future retrieval.

    Args:
        transcript_text: The full transcript text
        account_name: Customer account name (e.g., "Acme Corp")
        call_date: Date of the call (e.g., "2026-02-06")
        account_stage: Sales stage - Discovery, Evaluation, POC, Negotiation, Renewal, or Expansion
        products: Comma-separated products discussed (e.g., "Vault, Terraform")
        sentiment: Overall sentiment - Positive, Neutral, Cautious, or Negative
        summary: Brief 2-3 sentence summary of the call
    """
    doc_id = store_transcript(
        transcript_text=transcript_text,
        account_name=account_name,
        call_date=call_date,
        account_stage=account_stage,
        products=products,
        sentiment=sentiment,
        summary=summary,
    )

    return json.dumps({
        "status": "success",
        "document_id": doc_id,
        "message": f"Transcript for {account_name} stored successfully.",
    })
