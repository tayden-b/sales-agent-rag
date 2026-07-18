"""
Tests for the knowledge-base updater: chunk boundaries and the ChromaDB
metadata written per chunk. Fixture-based — a fake collection captures the
upsert, so nothing here touches ChromaDB or an embedding API.
"""

from src.rag.ingest import chunk_text, ingest_file


class FakeCollection:
    """Stand-in for a chromadb Collection that records the upsert args."""

    def __init__(self):
        self.calls = []

    def upsert(self, ids, documents, metadatas):
        self.calls.append({"ids": ids, "documents": documents, "metadatas": metadatas})


class TestChunkText:
    def test_single_paragraph_under_limit_is_one_chunk(self):
        chunks = chunk_text("alpha beta gamma", chunk_size=10, overlap=0)
        assert chunks == ["alpha beta gamma"]

    def test_splits_on_paragraph_boundary_when_size_exceeded(self):
        text = "a b c\n\nd e f"
        chunks = chunk_text(text, chunk_size=5, overlap=0)
        assert chunks == ["a b c", "d e f"]

    def test_overlap_carries_tail_words_into_next_chunk(self):
        text = "w1 w2 w3\n\nw4 w5 w6\n\nw7 w8 w9"
        chunks = chunk_text(text, chunk_size=5, overlap=2)
        # Second chunk starts with the last two words of the first.
        assert chunks[0] == "w1 w2 w3"
        assert chunks[1].split()[:2] == ["w2", "w3"]

    def test_whitespace_only_yields_no_chunks(self):
        assert chunk_text("   \n\n  ", chunk_size=10, overlap=0) == []

    def test_no_words_are_dropped(self):
        text = "one two\n\nthree four\n\nfive six"
        chunks = chunk_text(text, chunk_size=3, overlap=0)
        assert " ".join(chunks).split() == ["one", "two", "three", "four", "five", "six"]


class TestIngestMetadata:
    def test_single_chunk_metadata(self, tmp_path):
        doc = tmp_path / "auth-methods.md"
        doc.write_text("Vault supports many auth methods.", encoding="utf-8")
        collection = FakeCollection()

        stored = ingest_file(doc, "vault", collection=collection)

        assert stored == 1
        (call,) = collection.calls
        assert call["ids"] == ["vault_auth-methods_0"]
        assert call["documents"] == ["Vault supports many auth methods."]
        assert call["metadatas"] == [
            {"product": "vault", "source_file": "auth-methods.md", "chunk_index": 0, "total_chunks": 1}
        ]

    def test_multi_chunk_ids_and_indices(self, tmp_path):
        # 10 paragraphs of 200 words each = 2000 words, well over the 800-word
        # default chunk size, so this produces several chunks.
        doc = tmp_path / "big.md"
        doc.write_text("\n\n".join(["word " * 200 for _ in range(10)]), encoding="utf-8")
        collection = FakeCollection()

        stored = ingest_file(doc, "terraform", collection=collection)

        (call,) = collection.calls
        n = len(call["ids"])
        assert n > 1
        assert stored == n
        assert len(call["documents"]) == n
        assert call["ids"] == [f"terraform_big_{i}" for i in range(n)]
        assert [m["chunk_index"] for m in call["metadatas"]] == list(range(n))
        # total_chunks is the same n on every chunk's metadata.
        assert {m["total_chunks"] for m in call["metadatas"]} == {n}
        assert {m["product"] for m in call["metadatas"]} == {"terraform"}
        assert {m["source_file"] for m in call["metadatas"]} == {"big.md"}

    def test_empty_file_stores_nothing(self, tmp_path):
        doc = tmp_path / "empty.md"
        doc.write_text("   \n\n  ", encoding="utf-8")
        collection = FakeCollection()

        stored = ingest_file(doc, "vault", collection=collection)

        assert stored == 0
        assert collection.calls == []
