"""
CrewAI tool for searching HashiCorp documentation.
Used by the Documentation Researcher agent.
"""

import json
from crewai.tools import tool

from src.rag.search import search_docs


@tool("Search HashiCorp Documentation")
def search_hashicorp_docs(query: str, product: str = "") -> str:
    """Search the HashiCorp documentation database for relevant information.
    Use this to find documentation about Vault, Terraform, or Consul.

    Args:
        query: What to search for (e.g., "secret rotation", "state locking")
        product: Optional product filter - "vault", "terraform", or "consul"
    """
    product_filter = product if product else None
    results = search_docs(query=query, product=product_filter, n_results=5)

    if not results:
        return json.dumps({
            "query": query,
            "results": [],
            "message": "No documentation found. The docs collection may be empty.",
        })

    formatted = []
    for r in results:
        formatted.append({
            "content": r["document"][:500],  # Truncate long chunks for agent context
            "product": r["metadata"].get("product", "unknown"),
            "source_file": r["metadata"].get("source_file", "unknown"),
            "relevance_score": round(1 - (r["distance"] or 0), 3),  # Convert distance to similarity
        })

    return json.dumps({"query": query, "results": formatted})
