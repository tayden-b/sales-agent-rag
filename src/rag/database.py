"""
ChromaDB client setup and collection management.

Two collections:
  - hashicorp-docs: Pre-populated HashiCorp documentation
  - call-transcripts: Grows as transcripts are processed
"""

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from src.config import OPENAI_API_KEY, CHROMA_DB_PATH, EMBEDDING_MODEL

DOCS_COLLECTION = "hashicorp-docs"
TRANSCRIPTS_COLLECTION = "call-transcripts"


def get_embedding_function() -> OpenAIEmbeddingFunction:
    """Create an OpenAI embedding function for ChromaDB."""
    return OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name=EMBEDDING_MODEL,
    )


def get_chroma_client() -> chromadb.PersistentClient:
    """Create a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=CHROMA_DB_PATH)


def get_docs_collection() -> chromadb.Collection:
    """Get or create the hashicorp-docs collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=DOCS_COLLECTION,
        embedding_function=get_embedding_function(),
    )


def get_transcripts_collection() -> chromadb.Collection:
    """Get or create the call-transcripts collection."""
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=TRANSCRIPTS_COLLECTION,
        embedding_function=get_embedding_function(),
    )
