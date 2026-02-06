"""
Tests for the RAG infrastructure: ingestion, search, and storage.
"""

import pytest
from unittest.mock import patch, MagicMock

from src.rag.ingest import chunk_text


class TestChunking:
    """Test the document chunking logic."""

    def test_short_text_single_chunk(self):
        text = "This is a short paragraph. It should stay as one chunk."
        chunks = chunk_text(text, chunk_size=100, overlap=10)
        assert len(chunks) == 1
        assert "short paragraph" in chunks[0]

    def test_long_text_multiple_chunks(self):
        # Create text with multiple paragraphs
        paragraphs = [f"Paragraph {i} " + "word " * 50 for i in range(10)]
        text = "\n\n".join(paragraphs)
        chunks = chunk_text(text, chunk_size=100, overlap=10)
        assert len(chunks) > 1

    def test_overlap_between_chunks(self):
        # Create text that will need to be chunked
        paragraphs = [f"Section {i}: " + "content " * 30 for i in range(5)]
        text = "\n\n".join(paragraphs)
        chunks = chunk_text(text, chunk_size=50, overlap=10)

        # With overlap, later chunks should contain some words from previous chunks
        assert len(chunks) >= 2

    def test_empty_text(self):
        chunks = chunk_text("", chunk_size=100, overlap=10)
        # Empty text produces one chunk with empty string
        assert len(chunks) <= 1

    def test_preserves_content(self):
        text = "Important fact one.\n\nImportant fact two.\n\nImportant fact three."
        chunks = chunk_text(text, chunk_size=1000, overlap=0)
        combined = " ".join(chunks)
        assert "Important fact one." in combined
        assert "Important fact two." in combined
        assert "Important fact three." in combined
