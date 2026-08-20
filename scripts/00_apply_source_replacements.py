from __future__ import annotations

import csv
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.catalog import load_catalog, save_catalog, validate_catalog
from src.conservation_intelligence.paths import METADATA_PATH


REPLACEMENTS_PATH = PROJECT_ROOT / "data" / "source_replacements.csv"


def main() -> None:
    rows = load_catalog()
    by_id = {row["doc_id"]: row for row in rows}
    with REPLACEMENTS_PATH.open("r", encoding="utf-8", newline="") as replacements_file:
        replacements = list(csv.DictReader(replacements_file))

    for replacement in replacements:
        doc_id = replacement["doc_id"]
        if doc_id not in by_id:
            raise SystemExit(f"Replacement references unknown document ID: {doc_id}")
        row = by_id[doc_id]
        url = replacement["url"]
        note = f"Replacement: {replacement['note']} (verified at {replacement['verification_url']})."
        if row["url"] != url:
            row["url"] = url
            row["local_file"] = ""
            row["file_type"] = ""
            row["download_status"] = "pending"
            row["resolved_url"] = ""
            row["retrieved_at"] = ""
            row["checksum_sha256"] = ""
            row["extracted_file"] = ""
            row["extraction_status"] = ""
            row["page_count"] = ""
            row["extracted_characters"] = ""
            row["extraction_notes"] = ""
        if note not in row["notes"]:
            row["notes"] = "; ".join(part for part in (row["notes"], note) if part)
        print(f"{doc_id}: {url}")

    errors = validate_catalog(rows)
    if errors:
        raise SystemExit("Invalid source catalog after replacements:\n- " + "\n- ".join(errors))
    save_catalog(rows, METADATA_PATH)


if __name__ == "__main__":
    main()
