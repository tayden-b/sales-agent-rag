"""
Document ingestion pipeline.

Reads markdown/text files from data/docs/, chunks them,
and stores them in the hashicorp-docs ChromaDB collection.
"""

import os
import logging
from pathlib import Path

from src.rag.database import get_docs_collection

logger = logging.getLogger(__name__)

DOCS_DIR = Path(__file__).parent.parent.parent / "data" / "docs"
CHUNK_SIZE = 800  # approximate words per chunk
CHUNK_OVERLAP = 100  # words of overlap between chunks


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Split text into overlapping chunks by word count.
    Tries to break at paragraph boundaries when possible.
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk_words: list[str] = []

    for paragraph in paragraphs:
        paragraph_words = paragraph.split()

        # If adding this paragraph exceeds chunk size, save current chunk and start new one
        if len(current_chunk_words) + len(paragraph_words) > chunk_size and current_chunk_words:
            chunks.append(" ".join(current_chunk_words))
            # Keep overlap words from the end of the current chunk
            current_chunk_words = current_chunk_words[-overlap:] if overlap > 0 else []

        current_chunk_words.extend(paragraph_words)

    # Don't forget the last chunk
    if current_chunk_words:
        chunks.append(" ".join(current_chunk_words))

    return chunks


def ingest_file(file_path: Path, product: str) -> int:
    """
    Ingest a single documentation file into ChromaDB.
    Returns the number of chunks stored.
    """
    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        logger.warning(f"Skipping empty file: {file_path}")
        return 0

    chunks = chunk_text(text)
    collection = get_docs_collection()

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        doc_id = f"{product}_{file_path.stem}_{i}"
        ids.append(doc_id)
        documents.append(chunk)
        metadatas.append({
            "product": product,
            "source_file": file_path.name,
            "chunk_index": i,
            "total_chunks": len(chunks),
        })

    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
    logger.info(f"Ingested {len(chunks)} chunks from {file_path.name} (product: {product})")
    return len(chunks)


def ingest_all_docs() -> int:
    """
    Walk data/docs/ directory and ingest all files.
    Subdirectory names are used as the product tag (e.g., vault, terraform).
    Returns total chunks ingested.
    """
    total = 0

    if not DOCS_DIR.exists():
        logger.error(f"Documentation directory not found: {DOCS_DIR}")
        return 0

    for product_dir in sorted(DOCS_DIR.iterdir()):
        if not product_dir.is_dir():
            continue

        product = product_dir.name
        for doc_file in sorted(product_dir.glob("*.md")):
            total += ingest_file(doc_file, product)

        for doc_file in sorted(product_dir.glob("*.txt")):
            total += ingest_file(doc_file, product)

    logger.info(f"Ingestion complete. Total chunks: {total}")
    return total


if __name__ == "__main__":
    from src.config import setup_logging
    setup_logging()
    ingest_all_docs()
