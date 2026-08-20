from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.catalog import load_catalog, validate_catalog
from src.conservation_intelligence.chunking import chunk_text
from src.conservation_intelligence.database import connect_database, initialize_database
from src.conservation_intelligence.repository import replace_document_chunks, sync_documents
from src.conservation_intelligence.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build retrieval chunks in SQLite.")
    parser.add_argument("--doc-id", action="append", dest="doc_ids")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rows = load_catalog()
    errors = validate_catalog(rows)
    if errors:
        raise SystemExit("Invalid source catalog:\n- " + "\n- ".join(errors))
    settings = load_settings()
    initialize_database()

    selected = set(args.doc_ids) if args.doc_ids else None
    total_chunks = 0
    with connect_database() as connection:
        sync_documents(connection, rows)
        for row in rows:
            if selected is not None and row["doc_id"] not in selected:
                continue
            if row["extraction_status"] not in {"extracted", "low_text"}:
                print(f"{row['doc_id']}: skipped ({row['extraction_status'] or 'not extracted'})")
                continue
            text_path = PROJECT_ROOT / row["extracted_file"]
            chunks = chunk_text(
                row["doc_id"],
                text_path.read_text(encoding="utf-8"),
                target_words=settings.chunking.target_words,
                min_words=settings.chunking.min_words,
                max_words=settings.chunking.max_words,
                overlap_words=settings.chunking.overlap_words,
            )
            count = replace_document_chunks(connection, row, chunks)
            total_chunks += count
            print(f"{row['doc_id']}: {count} chunks")
    print(f"Total chunks built: {total_chunks}")


if __name__ == "__main__":
    main()

