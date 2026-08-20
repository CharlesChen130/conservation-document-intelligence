from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

from .catalog import save_catalog
from .paths import METADATA_PATH, PROCESSED_DIR, PROJECT_ROOT


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExtractionResult:
    doc_id: str
    status: str
    extracted_file: str = ""
    page_count: int = 0
    character_count: int = 0
    note: str = ""


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[\t \u00a0]+", " ", line).strip() for line in text.split("\n")]
    normalized: list[str] = []
    previous_blank = False
    for line in lines:
        is_blank = not line
        if is_blank and previous_blank:
            continue
        normalized.append(line)
        previous_blank = is_blank
    return "\n".join(normalized).strip()


def _resolve_local_file(row: dict[str, str], project_root: Path) -> Path:
    local_file = row.get("local_file", "")
    if not local_file:
        raise ValueError("source has no local_file")
    path = (project_root / local_file).resolve()
    if not path.is_relative_to(project_root.resolve()):
        raise ValueError("local_file resolves outside the project root")
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def _extract_pdf(path: Path) -> tuple[str, int, int, str]:
    reader = PdfReader(path)
    sections: list[str] = []
    character_count = 0
    empty_pages: list[int] = []
    page_errors: list[str] = []

    for page_number, page in enumerate(reader.pages, start=1):
        try:
            page_text = normalize_text(page.extract_text() or "")
        except Exception as error:
            page_text = ""
            page_errors.append(f"page {page_number}: {error}")
        if not page_text:
            empty_pages.append(page_number)
        character_count += len(page_text)
        sections.append(f"--- Page {page_number} ---\n\n{page_text}".rstrip())

    notes: list[str] = []
    if empty_pages:
        preview = ", ".join(str(number) for number in empty_pages[:10])
        suffix = "..." if len(empty_pages) > 10 else ""
        notes.append(f"{len(empty_pages)} empty pages ({preview}{suffix})")
    if page_errors:
        notes.append("; ".join(page_errors[:5]))
    return "\n\n".join(sections) + "\n", len(reader.pages), character_count, "; ".join(notes)


def _extract_text_file(path: Path) -> tuple[str, int, int, str]:
    raw_text = path.read_text(encoding="utf-8", errors="replace")
    text = normalize_text(raw_text)
    return f"--- Source Text ---\n\n{text}\n", 1, len(text), "HTML/text sources have no PDF page number."


def extract_source(
    row: dict[str, str],
    *,
    project_root: Path = PROJECT_ROOT,
    processed_dir: Path = PROCESSED_DIR,
    force: bool = False,
    low_text_threshold: int = 500,
) -> ExtractionResult:
    doc_id = row["doc_id"]
    existing_file = row.get("extracted_file", "")
    if not force and row.get("extraction_status") in {"extracted", "low_text"} and existing_file:
        existing_path = project_root / existing_file
        if existing_path.is_file():
            return ExtractionResult(
                doc_id=doc_id,
                status="unchanged",
                extracted_file=existing_file,
                page_count=int(row.get("page_count") or 0),
                character_count=int(row.get("extracted_characters") or 0),
                note="Existing extracted text retained.",
            )

    try:
        source_path = _resolve_local_file(row, project_root)
        if row.get("file_type") == "pdf" or source_path.suffix.lower() == ".pdf":
            text, page_count, character_count, note = _extract_pdf(source_path)
        else:
            text, page_count, character_count, note = _extract_text_file(source_path)

        status = "extracted" if character_count >= low_text_threshold else "low_text"
        if status == "low_text":
            warning = f"Only {character_count} characters extracted; OCR or replacement review may be needed."
            note = "; ".join(part for part in (note, warning) if part)

        processed_dir.mkdir(parents=True, exist_ok=True)
        destination = processed_dir / f"{doc_id}.txt"
        temporary = destination.with_suffix(".txt.part")
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(destination)
        return ExtractionResult(
            doc_id=doc_id,
            status=status,
            extracted_file=destination.relative_to(project_root).as_posix(),
            page_count=page_count,
            character_count=character_count,
            note=note,
        )
    except Exception as error:
        LOGGER.warning("Failed to extract %s: %s", doc_id, error)
        return ExtractionResult(doc_id=doc_id, status="failed", note=str(error))


def extract_catalog(
    rows: list[dict[str, str]],
    selected_ids: Iterable[str] | None = None,
    *,
    force: bool = False,
    catalog_path: Path = METADATA_PATH,
) -> list[ExtractionResult]:
    selected = set(selected_ids) if selected_ids is not None else None
    results: list[ExtractionResult] = []

    for row in rows:
        if selected is not None and row["doc_id"] not in selected:
            continue
        result = extract_source(row, force=force)
        results.append(result)
        if result.status == "unchanged":
            continue
        row["extraction_status"] = result.status
        row["extracted_file"] = result.extracted_file
        row["page_count"] = str(result.page_count) if result.page_count else ""
        row["extracted_characters"] = (
            str(result.character_count) if result.character_count else ""
        )
        row["extraction_notes"] = result.note
        save_catalog(rows, catalog_path)

    return results

