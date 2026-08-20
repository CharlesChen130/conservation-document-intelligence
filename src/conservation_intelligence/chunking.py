from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


PAGE_MARKER = re.compile(r"^--- Page (\d+) ---$", re.MULTILINE)
SOURCE_MARKER = "--- Source Text ---"
WORD = re.compile(r"\S+")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    page: str
    text: str
    word_count: int
    content_hash: str


def parse_page_tokens(text: str) -> list[tuple[str, int | None]]:
    tokens: list[tuple[str, int | None]] = []
    current_page: int | None = None
    position = 0

    markers = list(PAGE_MARKER.finditer(text))
    if markers:
        for marker_index, marker in enumerate(markers):
            section_start = marker.end()
            section_end = markers[marker_index + 1].start() if marker_index + 1 < len(markers) else len(text)
            current_page = int(marker.group(1))
            tokens.extend((match.group(0), current_page) for match in WORD.finditer(text[section_start:section_end]))
        return tokens

    if text.startswith(SOURCE_MARKER):
        position = len(SOURCE_MARKER)
    tokens.extend((match.group(0), current_page) for match in WORD.finditer(text[position:]))
    return tokens


def format_page_range(pages: list[int | None]) -> str:
    numbered = [page for page in pages if page is not None]
    if not numbered:
        return ""
    first = min(numbered)
    last = max(numbered)
    return str(first) if first == last else f"{first}-{last}"


def chunk_text(
    doc_id: str,
    text: str,
    *,
    target_words: int = 750,
    min_words: int = 600,
    max_words: int = 900,
    overlap_words: int = 100,
) -> list[Chunk]:
    if not 0 <= overlap_words < min_words <= target_words <= max_words:
        raise ValueError("invalid chunk-size configuration")

    tokens = parse_page_tokens(text)
    if not tokens:
        return []

    chunks: list[Chunk] = []
    start = 0
    total = len(tokens)
    while start < total:
        end = min(start + target_words, total)
        window = tokens[start:end]
        chunk_value = " ".join(token for token, _ in window)
        chunk_number = len(chunks) + 1
        chunks.append(
            Chunk(
                chunk_id=f"{doc_id}-C{chunk_number:04d}",
                doc_id=doc_id,
                page=format_page_range([page for _, page in window]),
                text=chunk_value,
                word_count=len(window),
                content_hash=hashlib.sha256(chunk_value.encode("utf-8")).hexdigest(),
            )
        )
        if end == total:
            break

        next_start = end - overlap_words
        remaining = total - next_start
        if remaining < min_words:
            next_start = max(start + 1, total - min(target_words, total))
        start = next_start

    return chunks

