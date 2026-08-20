from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass, replace
from typing import Iterable, Sequence

from .chunking import Chunk


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "by",
    "do",
    "does",
    "for",
    "from",
    "how",
    "in",
    "is",
    "of",
    "or",
    "the",
    "than",
    "to",
    "what",
    "which",
    "who",
    "with",
}

REFERENCE_HEADING_RE = re.compile(
    r"\b(?:bibliography|cited references|literature cited|references)\b",
    flags=re.IGNORECASE,
)
TABLE_OF_CONTENTS_RE = re.compile(r"\btable of contents\b", flags=re.IGNORECASE)


@dataclass(frozen=True)
class SearchResult:
    chunk_id: str
    doc_id: str
    title: str
    page: str
    text: str
    source_url: str
    score: float


def evidence_quality_issues(text: str) -> list[str]:
    """Identify chunks that are unsafe as synthesis evidence but remain searchable."""
    normalized = " ".join(text.split())
    lowered = normalized.casefold()
    issues: list[str] = []
    doi_count = lowered.count("doi.org") + lowered.count("doi:")
    year_count = len(re.findall(r"\b(?:19|20)\d{2}[a-z]?\b", normalized))
    if REFERENCE_HEADING_RE.search(normalized) and (doi_count >= 2 or year_count >= 8):
        issues.append("reference_section")
    elif doi_count >= 4 and year_count >= 6:
        issues.append("reference_section")
    dot_leaders = len(re.findall(r"(?:\.\s*){5,}", normalized))
    if TABLE_OF_CONTENTS_RE.search(normalized) and dot_leaders:
        issues.append("table_of_contents")
    return issues


def filter_high_information_results(
    results: Sequence[SearchResult],
) -> list[SearchResult]:
    """Remove bibliography/TOC chunks from answer evidence without altering the index."""
    return [result for result in results if not evidence_quality_issues(result.text)]


def sync_documents(connection: sqlite3.Connection, rows: Iterable[dict[str, str]]) -> int:
    values = [
        (
            row["doc_id"],
            row["title"],
            row["year"],
            row["agency"],
            row["topic"],
            row["url"],
            row["local_file"],
            row["file_type"],
            row["original_url"],
            row["resolved_url"],
            row["download_status"],
            row["notes"],
            row["checksum_sha256"],
            row["retrieved_at"],
        )
        for row in rows
    ]
    connection.executemany(
        """
        INSERT INTO documents (
            doc_id, title, year, agency, topic, url, local_file, file_type,
            original_url, resolved_url, download_status, notes, checksum_sha256, retrieved_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(doc_id) DO UPDATE SET
            title=excluded.title,
            year=excluded.year,
            agency=excluded.agency,
            topic=excluded.topic,
            url=excluded.url,
            local_file=excluded.local_file,
            file_type=excluded.file_type,
            original_url=excluded.original_url,
            resolved_url=excluded.resolved_url,
            download_status=excluded.download_status,
            notes=excluded.notes,
            checksum_sha256=excluded.checksum_sha256,
            retrieved_at=excluded.retrieved_at
        """,
        values,
    )
    return len(values)


def replace_document_chunks(
    connection: sqlite3.Connection,
    document: dict[str, str],
    chunks: Sequence[Chunk],
) -> int:
    doc_id = document["doc_id"]
    existing_ids = [
        row[0]
        for row in connection.execute("SELECT chunk_id FROM chunks WHERE doc_id = ?", (doc_id,))
    ]
    if existing_ids:
        connection.executemany("DELETE FROM chunks_fts WHERE chunk_id = ?", ((item,) for item in existing_ids))
    connection.execute("DELETE FROM chunks WHERE doc_id = ?", (doc_id,))

    chunk_rows = [
        (
            chunk.chunk_id,
            doc_id,
            chunk.page,
            chunk.text,
            document.get("resolved_url") or document["url"],
            document["title"],
            chunk.word_count,
            chunk.content_hash,
        )
        for chunk in chunks
    ]
    connection.executemany(
        """
        INSERT INTO chunks (
            chunk_id, doc_id, page, chunk_text, source_url, title, word_count, content_hash
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        chunk_rows,
    )
    connection.executemany(
        "INSERT INTO chunks_fts (chunk_id, title, chunk_text) VALUES (?, ?, ?)",
        ((row[0], row[5], row[3]) for row in chunk_rows),
    )
    return len(chunk_rows)


def _fts_query(value: str) -> str:
    tokens = re.findall(r"[\w'-]+", value, flags=re.UNICODE)
    tokens = [
        token
        for token in tokens
        if token.casefold() not in STOPWORDS and len(token) > 1
    ]
    return " OR ".join(f'"{token.replace(chr(34), "")}"' for token in tokens)


def keyword_search(
    connection: sqlite3.Connection,
    query: str,
    *,
    limit: int = 10,
    agency: str | None = None,
    topic: str | None = None,
) -> list[SearchResult]:
    match_query = _fts_query(query)
    if not match_query:
        return []

    filters = ["chunks_fts MATCH ?"]
    parameters: list[object] = [match_query]
    if agency:
        filters.append("d.agency = ?")
        parameters.append(agency)
    if topic:
        filters.append("d.topic = ?")
        parameters.append(topic)
    parameters.append(limit)

    rows = connection.execute(
        f"""
        SELECT c.chunk_id, c.doc_id, c.title, c.page, c.chunk_text, c.source_url,
               bm25(chunks_fts, 0.0, 2.0, 1.0) AS rank
        FROM chunks_fts
        JOIN chunks AS c ON c.chunk_id = chunks_fts.chunk_id
        JOIN documents AS d ON d.doc_id = c.doc_id
        WHERE {' AND '.join(filters)}
        ORDER BY rank
        LIMIT ?
        """,
        parameters,
    ).fetchall()
    return [
        SearchResult(
            chunk_id=row["chunk_id"],
            doc_id=row["doc_id"],
            title=row["title"],
            page=row["page"] or "",
            text=row["chunk_text"],
            source_url=row["source_url"],
            score=float(-row["rank"]),
        )
        for row in rows
    ]


def diversify_results(
    results: Sequence[SearchResult],
    *,
    limit: int,
    max_per_document: int = 2,
) -> list[SearchResult]:
    """Keep ranked results while preventing one long document from crowding out others."""
    selected: list[SearchResult] = []
    per_document: dict[str, int] = {}
    for result in results:
        count = per_document.get(result.doc_id, 0)
        if count >= max_per_document:
            continue
        selected.append(result)
        per_document[result.doc_id] = count + 1
        if len(selected) == limit:
            break
    return selected


def reciprocal_rank_fusion(
    *rankings: Sequence[SearchResult],
    rank_constant: float = 60.0,
) -> list[SearchResult]:
    """Fuse independent ranked lists without comparing incompatible raw scores.

    BM25 and cosine-similarity scores have different scales. Reciprocal Rank
    Fusion uses only each result's position, so neither retrieval backend can
    dominate merely because of its score range.
    """
    if rank_constant <= 0:
        raise ValueError("rank_constant must be positive")
    scores: dict[str, float] = {}
    records: dict[str, SearchResult] = {}
    first_seen: dict[str, int] = {}
    order = 0
    for ranking in rankings:
        seen_in_ranking: set[str] = set()
        for rank, result in enumerate(ranking, start=1):
            if result.chunk_id in seen_in_ranking:
                continue
            seen_in_ranking.add(result.chunk_id)
            if result.chunk_id not in records:
                records[result.chunk_id] = result
                first_seen[result.chunk_id] = order
                order += 1
            scores[result.chunk_id] = scores.get(result.chunk_id, 0.0) + (
                1.0 / (rank_constant + rank)
            )
    return [
        replace(records[chunk_id], score=scores[chunk_id])
        for chunk_id in sorted(
            records,
            key=lambda item: (-scores[item], first_seen[item]),
        )
    ]


def fetch_adjacent_chunks(
    connection: sqlite3.Connection,
    chunk_ids: Sequence[str],
    *,
    window: int = 1,
) -> list[SearchResult]:
    """Load neighboring chunks to recover evidence split at chunk boundaries."""
    if window < 0:
        raise ValueError("window cannot be negative")
    requested = set(chunk_ids)
    adjacent_ids: list[str] = []
    for chunk_id in dict.fromkeys(chunk_ids):
        match = re.fullmatch(r"(DOC\d{3})-C(\d{4})", chunk_id)
        if not match:
            continue
        document_id, number_text = match.groups()
        number = int(number_text)
        for offset in range(-window, window + 1):
            if offset == 0 or number + offset < 1:
                continue
            adjacent_id = f"{document_id}-C{number + offset:04d}"
            if adjacent_id not in requested and adjacent_id not in adjacent_ids:
                adjacent_ids.append(adjacent_id)
    return fetch_chunks(connection, adjacent_ids)


def fetch_chunks(
    connection: sqlite3.Connection,
    chunk_ids: Sequence[str],
) -> list[SearchResult]:
    """Load exact stored chunks in caller-provided order for wiki evidence resolution."""
    ordered_ids = list(dict.fromkeys(chunk_ids))
    if not ordered_ids:
        return []
    placeholders = ", ".join("?" for _ in ordered_ids)
    rows = connection.execute(
        f"""
        SELECT chunk_id, doc_id, title, page, chunk_text, source_url
        FROM chunks
        WHERE chunk_id IN ({placeholders})
        """,
        ordered_ids,
    ).fetchall()
    by_id = {row["chunk_id"]: row for row in rows}
    return [
        SearchResult(
            chunk_id=by_id[chunk_id]["chunk_id"],
            doc_id=by_id[chunk_id]["doc_id"],
            title=by_id[chunk_id]["title"],
            page=by_id[chunk_id]["page"] or "",
            text=by_id[chunk_id]["chunk_text"],
            source_url=by_id[chunk_id]["source_url"],
            score=0.0,
        )
        for chunk_id in ordered_ids
        if chunk_id in by_id
    ]
