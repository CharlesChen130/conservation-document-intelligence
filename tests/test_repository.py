from __future__ import annotations

from src.conservation_intelligence.chunking import Chunk
from src.conservation_intelligence.database import connect_database, initialize_database
from src.conservation_intelligence.repository import (
    SearchResult,
    diversify_results,
    evidence_quality_issues,
    fetch_adjacent_chunks,
    fetch_chunks,
    filter_high_information_results,
    keyword_search,
    replace_document_chunks,
    reciprocal_rank_fusion,
    sync_documents,
)


def _document() -> dict[str, str]:
    return {
        "doc_id": "DOC999",
        "title": "Wetland Test Plan",
        "year": "2026",
        "agency": "Test Agency",
        "topic": "Wetlands",
        "url": "https://example.org/source",
        "local_file": "data/raw/DOC999.txt",
        "file_type": "html_text",
        "original_url": "https://example.org/source",
        "resolved_url": "https://example.org/source",
        "download_status": "downloaded",
        "notes": "",
        "checksum_sha256": "abc",
        "retrieved_at": "2026-01-01T00:00:00+00:00",
    }


def test_keyword_search_returns_traceable_chunk(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    chunk = Chunk(
        chunk_id="DOC999-C0001",
        doc_id="DOC999",
        page="3",
        text="Wetland restoration improves habitat for waterfowl.",
        word_count=7,
        content_hash="hash",
    )

    with connect_database(database_path) as connection:
        document = _document()
        sync_documents(connection, [document])
        replace_document_chunks(connection, document, [chunk])
        results = keyword_search(connection, "wetland habitat")

    assert len(results) == 1
    assert results[0].doc_id == "DOC999"
    assert results[0].page == "3"
    assert results[0].source_url == "https://example.org/source"

    with connect_database(database_path) as connection:
        exact = fetch_chunks(connection, ["DOC999-C0001", "missing"])
    assert [result.chunk_id for result in exact] == ["DOC999-C0001"]


def test_diversify_results_limits_chunks_per_document():
    def result(chunk_id: str, doc_id: str, score: float) -> SearchResult:
        return SearchResult(chunk_id, doc_id, doc_id, "1", "text", "https://example.org", score)

    ranked = [
        result("A1", "DOCA", 4.0),
        result("A2", "DOCA", 3.0),
        result("A3", "DOCA", 2.0),
        result("B1", "DOCB", 1.0),
    ]

    selected = diversify_results(ranked, limit=3, max_per_document=2)

    assert [item.chunk_id for item in selected] == ["A1", "A2", "B1"]


def test_reciprocal_rank_fusion_rewards_results_found_by_both_backends():
    def result(chunk_id: str, score: float) -> SearchResult:
        return SearchResult(
            chunk_id,
            "DOC999",
            "Title",
            "1",
            "text",
            "https://example.org",
            score,
        )

    keyword = [result("K", 100.0), result("BOTH", 1.0)]
    semantic = [result("S", 0.99), result("BOTH", 0.2)]

    fused = reciprocal_rank_fusion(keyword, semantic)

    assert [item.chunk_id for item in fused] == ["BOTH", "K", "S"]
    assert fused[0].score > fused[1].score


def test_fetch_adjacent_chunks_recovers_chunk_boundary_neighbors(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)
    document = _document()
    chunks = [
        Chunk(
            f"DOC999-C{number:04d}",
            "DOC999",
            str(number),
            f"Evidence part {number}.",
            3,
            f"hash-{number}",
        )
        for number in range(1, 4)
    ]
    with connect_database(database_path) as connection:
        sync_documents(connection, [document])
        replace_document_chunks(connection, document, chunks)
        adjacent = fetch_adjacent_chunks(connection, ["DOC999-C0002"])

    assert [item.chunk_id for item in adjacent] == [
        "DOC999-C0001",
        "DOC999-C0003",
    ]


def test_evidence_quality_filter_rejects_references_and_table_of_contents():
    references = (
        "References Smith, A., 2019. Study. https://doi.org/10.1/a. "
        "Jones, B., 2020. Study. https://doi.org/10.1/b. "
        + " ".join(f"Author {year}." for year in range(2010, 2018))
    )
    contents = "TABLE OF CONTENTS Wetland Conservation . . . . . . . . . 42"
    useful = "Wetland restoration requires hydrologic monitoring and native vegetation."

    assert "reference_section" in evidence_quality_issues(references)
    assert "table_of_contents" in evidence_quality_issues(contents)
    results = [
        SearchResult("R", "DOC1", "Refs", "1", references, "https://example.org", 3.0),
        SearchResult("T", "DOC2", "TOC", "2", contents, "https://example.org", 2.0),
        SearchResult("U", "DOC3", "Plan", "3", useful, "https://example.org", 1.0),
    ]

    assert [item.chunk_id for item in filter_high_information_results(results)] == ["U"]
