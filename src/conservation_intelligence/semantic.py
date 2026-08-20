from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol, Sequence

import faiss
import numpy as np
from openai import OpenAI

from .database import connect_database
from .paths import DATABASE_PATH, FAISS_INDEX_PATH, FAISS_MANIFEST_PATH
from .repository import SearchResult


class EmbeddingProvider(Protocol):
    model: str

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


@dataclass
class OpenAIEmbeddingProvider:
    model: str = "text-embedding-3-small"
    api_key: str | None = None
    timeout_seconds: float = 30.0
    max_retries: int = 0
    input_tokens_used: int = field(init=False, default=0)

    def __post_init__(self) -> None:
        key = self.api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise ValueError("OPENAI_API_KEY is required to create OpenAI embeddings")
        self._client = OpenAI(
            api_key=key,
            timeout=self.timeout_seconds,
            max_retries=self.max_retries,
        )

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self._client.embeddings.create(
            model=self.model,
            input=list(texts),
            encoding_format="float",
        )
        usage = getattr(response, "usage", None)
        self.input_tokens_used += int(
            getattr(usage, "prompt_tokens", 0)
            or getattr(usage, "total_tokens", 0)
            or 0
        )
        ordered = sorted(response.data, key=lambda item: item.index)
        return [item.embedding for item in ordered]


def corpus_digest(records: Sequence[tuple[str, str]]) -> str:
    digest = hashlib.sha256()
    for chunk_id, content_hash in records:
        digest.update(chunk_id.encode("utf-8"))
        digest.update(b"\0")
        digest.update(content_hash.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def build_faiss_index(
    provider: EmbeddingProvider,
    *,
    database_path: Path = DATABASE_PATH,
    index_path: Path = FAISS_INDEX_PATH,
    manifest_path: Path = FAISS_MANIFEST_PATH,
    batch_size: int = 64,
) -> dict[str, object]:
    with connect_database(database_path) as connection:
        rows = connection.execute(
            "SELECT chunk_id, chunk_text, content_hash FROM chunks ORDER BY chunk_id"
        ).fetchall()
    if not rows:
        raise ValueError("No chunks are available; run scripts/03_build_chunks.py first")

    vectors: list[list[float]] = []
    for start in range(0, len(rows), batch_size):
        batch = [row["chunk_text"] for row in rows[start : start + batch_size]]
        vectors.extend(provider.embed(batch))
    if len(vectors) != len(rows):
        raise ValueError("Embedding provider returned an unexpected number of vectors")

    matrix = np.asarray(vectors, dtype="float32")
    if matrix.ndim != 2 or matrix.shape[1] == 0:
        raise ValueError("Embedding provider returned invalid vectors")
    faiss.normalize_L2(matrix)
    index = faiss.IndexFlatIP(matrix.shape[1])
    index.add(matrix)

    records = [(row["chunk_id"], row["content_hash"] or "") for row in rows]
    manifest: dict[str, object] = {
        "schema_version": 1,
        "model": provider.model,
        "dimension": int(matrix.shape[1]),
        "chunk_count": len(rows),
        "chunk_ids": [row["chunk_id"] for row in rows],
        "corpus_digest": corpus_digest(records),
        "built_at": datetime.now(timezone.utc).isoformat(),
    }

    index_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_index = index_path.with_suffix(".faiss.part")
    temporary_manifest = manifest_path.with_suffix(".json.part")
    faiss.write_index(index, str(temporary_index))
    temporary_manifest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    temporary_index.replace(index_path)
    temporary_manifest.replace(manifest_path)
    return manifest


def load_manifest(path: Path = FAISS_MANIFEST_PATH) -> dict[str, object]:
    if not path.is_file():
        raise FileNotFoundError("Semantic index manifest does not exist")
    return json.loads(path.read_text(encoding="utf-8"))


def semantic_index_is_current(
    *,
    database_path: Path = DATABASE_PATH,
    manifest_path: Path = FAISS_MANIFEST_PATH,
) -> bool:
    try:
        manifest = load_manifest(manifest_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return False
    with connect_database(database_path) as connection:
        rows = connection.execute(
            "SELECT chunk_id, content_hash FROM chunks ORDER BY chunk_id"
        ).fetchall()
    records = [(row["chunk_id"], row["content_hash"] or "") for row in rows]
    return manifest.get("corpus_digest") == corpus_digest(records)


def semantic_search(
    provider: EmbeddingProvider,
    query: str,
    *,
    limit: int = 10,
    database_path: Path = DATABASE_PATH,
    index_path: Path = FAISS_INDEX_PATH,
    manifest_path: Path = FAISS_MANIFEST_PATH,
) -> list[SearchResult]:
    if not query.strip():
        return []
    manifest = load_manifest(manifest_path)
    if manifest.get("model") != provider.model:
        raise ValueError(
            f"Index model is {manifest.get('model')!r}, but query provider uses {provider.model!r}"
        )
    index = faiss.read_index(str(index_path))
    query_vector = np.asarray(provider.embed([query]), dtype="float32")
    if query_vector.shape != (1, index.d):
        raise ValueError("Query embedding dimension does not match the index")
    faiss.normalize_L2(query_vector)
    scores, positions = index.search(query_vector, min(limit, index.ntotal))

    chunk_ids = manifest.get("chunk_ids")
    if not isinstance(chunk_ids, list):
        raise ValueError("Semantic index manifest has no chunk ID mapping")
    selected = [
        (chunk_ids[position], float(score))
        for position, score in zip(positions[0], scores[0])
        if position >= 0
    ]
    if not selected:
        return []

    placeholders = ",".join("?" for _ in selected)
    with connect_database(database_path) as connection:
        rows = connection.execute(
            f"""
            SELECT chunk_id, doc_id, title, page, chunk_text, source_url
            FROM chunks WHERE chunk_id IN ({placeholders})
            """,
            [chunk_id for chunk_id, _ in selected],
        ).fetchall()
    by_id = {row["chunk_id"]: row for row in rows}
    return [
        SearchResult(
            chunk_id=chunk_id,
            doc_id=by_id[chunk_id]["doc_id"],
            title=by_id[chunk_id]["title"],
            page=by_id[chunk_id]["page"] or "",
            text=by_id[chunk_id]["chunk_text"],
            source_url=by_id[chunk_id]["source_url"],
            score=score,
        )
        for chunk_id, score in selected
        if chunk_id in by_id
    ]
