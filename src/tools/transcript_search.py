"""
CrewAI tool for searching past call transcripts.
Used by the Historical Context Analyst agent.
"""

import json
from crewai.tools import tool

from src.rag.search import search_transcripts


@tool("Search Past Call Transcripts")
def search_past_transcripts(query: str, account_stage: str = "", product: str = "") -> str:
    """Search past call transcripts for similar situations, patterns, and context.
    Use this to find how similar deals or technical concerns were handled before.

    Args:
        query: What to search for (e.g., "vault migration concerns", "terraform adoption")
        account_stage: Optional stage filter - "Discovery", "Evaluation", "POC", "Negotiation", "Renewal", "Expansion"
        product: Optional product filter - "vault", "terraform", "consul"
    """
    stage_filter = account_stage if account_stage else None
    product_filter = product if product else None

    results = search_transcripts(
        query=query,
        account_stage=stage_filter,
        product=product_filter,
        n_results=5,
    )

    if not results:
        return json.dumps({
            "query": query,
            "results": [],
            "message": "No past transcripts found. The knowledge base will grow as more calls are processed.",
        })

    formatted = []
    for r in results:
        formatted.append({
            "content": r["document"],
            "account_name": r["metadata"].get("account_name", "unknown"),
            "call_date": r["metadata"].get("call_date", "unknown"),
            "account_stage": r["metadata"].get("account_stage", "unknown"),
            "products": r["metadata"].get("products", "unknown"),
            "sentiment": r["metadata"].get("sentiment", "unknown"),
            "relevance_score": round(1 - (r["distance"] or 0), 3),
        })

    return json.dumps({"query": query, "results": formatted})
