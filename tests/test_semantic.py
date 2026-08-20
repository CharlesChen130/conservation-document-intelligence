from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from src.conservation_intelligence.chunking import Chunk
from src.conservation_intelligence.database import connect_database, initialize_database
from src.conservation_intelligence.repository import replace_document_chunks, sync_documents
from src.conservation_intelligence.semantic import (
    build_faiss_index,
    semantic_index_is_current,
    semantic_search,
)


@dataclass
class FakeEmbeddingProvider:
    model: str = "fake-embedding"

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        vectors = []
        for text in texts:
            lowered = text.lower()
            vectors.append(
                [
                    float(lowered.count("wetland") + lowered.count("waterfowl")),
                    float(lowered.count("invasive") + lowered.count("carp")),
                ]
            )
        return vectors


def _document(doc_id: str, title: str) -> dict[str, str]:
    return {
        "doc_id": doc_id,
        "title": title,
        "year": "2026",
        "agency": "Test Agency",
        "topic": "Test",
        "url": f"https://example.org/{doc_id}",
        "local_file": f"data/raw/{doc_id}.txt",
        "file_type": "html_text",
        "original_url": f"https://example.org/{doc_id}",
        "resolved_url": f"https://example.org/{doc_id}",
        "download_status": "downloaded",
        "notes": "",
        "checksum_sha256": "abc",
        "retrieved_at": "2026-01-01T00:00:00+00:00",
    }


def test_build_and_query_semantic_index(tmp_path: Path):
    database_path = tmp_path / "test.db"
    index_path = tmp_path / "chunks.faiss"
    manifest_path = tmp_path / "manifest.json"
    initialize_database(database_path)
    wetland = _document("DOC901", "Wetland Plan")
    invasive = _document("DOC902", "Invasive Carp Plan")

    with connect_database(database_path) as connection:
        sync_documents(connection, [wetland, invasive])
        replace_document_chunks(
            connection,
            wetland,
            [Chunk("DOC901-C0001", "DOC901", "1", "wetland waterfowl habitat", 3, "wet")],
        )
        replace_document_chunks(
            connection,
            invasive,
            [Chunk("DOC902-C0001", "DOC902", "2", "invasive carp control", 3, "carp")],
        )

    provider = FakeEmbeddingProvider()
    manifest = build_faiss_index(
        provider,
        database_path=database_path,
        index_path=index_path,
        manifest_path=manifest_path,
        batch_size=1,
    )
    results = semantic_search(
        provider,
        "carp invasive",
        limit=1,
        database_path=database_path,
        index_path=index_path,
        manifest_path=manifest_path,
    )

    assert manifest["chunk_count"] == 2
    assert semantic_index_is_current(
        database_path=database_path, manifest_path=manifest_path
    )
    assert results[0].doc_id == "DOC902"

