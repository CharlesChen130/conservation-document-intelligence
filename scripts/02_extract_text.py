from __future__ import annotations

import argparse
import logging
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.catalog import load_catalog, validate_catalog
from src.conservation_intelligence.extraction import extract_catalog
from src.conservation_intelligence.paths import ensure_directories


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract page-aware text from acquired sources.")
    parser.add_argument(
        "--doc-id",
        action="append",
        dest="doc_ids",
        help="Extract only this ID; may be repeated.",
    )
    parser.add_argument("--limit", type=int, help="Extract only the first N selected records.")
    parser.add_argument("--force", action="store_true", help="Re-extract existing processed text.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    ensure_directories()
    rows = load_catalog()
    errors = validate_catalog(rows)
    if errors:
        raise SystemExit("Invalid source catalog:\n- " + "\n- ".join(errors))

    selected_ids = args.doc_ids
    if args.limit is not None:
        available = selected_ids or [row["doc_id"] for row in rows]
        selected_ids = available[: args.limit]

    results = extract_catalog(rows, selected_ids=selected_ids, force=args.force)
    for result in results:
        detail = result.extracted_file or result.note
        print(
            f"{result.doc_id}: {result.status} pages={result.page_count} "
            f"characters={result.character_count} {detail}"
        )
    counts = Counter(result.status for result in results)
    print("Summary: " + ", ".join(f"{status}={count}" for status, count in sorted(counts.items())))


if __name__ == "__main__":
    main()

