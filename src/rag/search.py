"""
Semantic search over ChromaDB collections.
Used by agent tools to find relevant docs and past transcripts.
"""

import logging

from src.rag.database import get_docs_collection, get_transcripts_collection

logger = logging.getLogger(__name__)


def search_docs(query: str, product: str | None = None, n_results: int = 5) -> list[dict]:
    """
    Search the hashicorp-docs collection.

    Args:
        query: Search query text
        product: Optional filter by product (e.g., "vault", "terraform")
        n_results: Number of results to return

    Returns:
        List of dicts with keys: document, metadata, distance
    """
    collection = get_docs_collection()

    if collection.count() == 0:
        logger.warning("hashicorp-docs collection is empty. Run ingestion first.")
        return []

    where_filter = {"product": product} if product else None

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
    )

    return _format_results(results)


def search_transcripts(
    query: str,
    account_stage: str | None = None,
    product: str | None = None,
    n_results: int = 5,
) -> list[dict]:
    """
    Search the call-transcripts collection.

    Args:
        query: Search query text
        account_stage: Optional filter by stage (e.g., "Evaluation", "POC")
        product: Optional filter by product discussed
        n_results: Number of results to return

    Returns:
        List of dicts with keys: document, metadata, distance
    """
    collection = get_transcripts_collection()

    if collection.count() == 0:
        logger.info("call-transcripts collection is empty. No historical data yet.")
        return []

    # Build where filter for metadata
    where_filter = None
    if account_stage and product:
        where_filter = {
            "$and": [
                {"account_stage": account_stage},
                {"products": {"$contains": product}},
            ]
        }
    elif account_stage:
        where_filter = {"account_stage": account_stage}
    elif product:
        where_filter = {"products": {"$contains": product}}

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where_filter,
    )

    return _format_results(results)


def store_transcript(
    transcript_text: str,
    account_name: str,
    call_date: str,
    account_stage: str,
    products: str,
    sentiment: str,
    summary: str,
) -> str:
    """
    Store a processed transcript in the call-transcripts collection.

    Args:
        transcript_text: The full transcript text
        account_name: Customer account name
        call_date: Date of the call
        account_stage: Sales stage (Discovery, Evaluation, etc.)
        products: Comma-separated products discussed
        sentiment: Overall call sentiment
        summary: Brief summary for retrieval context

    Returns:
        The document ID of the stored transcript
    """
    collection = get_transcripts_collection()

    doc_id = f"transcript_{account_name}_{call_date}".replace(" ", "_").lower()

    # Store the summary as the searchable document (more useful for retrieval
    # than the raw transcript), with the full transcript available in metadata
    collection.upsert(
        ids=[doc_id],
        documents=[f"Account: {account_name}. Stage: {account_stage}. "
                   f"Products: {products}. Sentiment: {sentiment}. "
                   f"Summary: {summary}"],
        metadatas=[{
            "account_name": account_name,
            "call_date": call_date,
            "account_stage": account_stage,
            "products": products,
            "sentiment": sentiment,
        }],
    )

    logger.info(f"Stored transcript for {account_name} ({call_date}) as {doc_id}")
    return doc_id


def _format_results(results: dict) -> list[dict]:
    """Convert ChromaDB query results into a clean list of dicts."""
    formatted = []
    if not results or not results.get("documents"):
        return formatted

    for i, doc in enumerate(results["documents"][0]):
        entry = {
            "document": doc,
            "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
            "distance": results["distances"][0][i] if results.get("distances") else None,
        }
        formatted.append(entry)

    return formatted
