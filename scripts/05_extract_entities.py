from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.entity_extraction import extract_database, export_extractions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract evidence-backed conservation entities and relationships."
    )
    parser.add_argument("--doc-id", action="append", dest="doc_ids")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    entities, relations = extract_database(selected_ids=args.doc_ids)
    entities_path, relations_path = export_extractions()
    entity_types = Counter(item.entity_type for item in entities)
    relation_types = Counter(item.relation for item in relations)
    print(f"Extracted {len(entities)} entity mentions: {dict(sorted(entity_types.items()))}")
    print(f"Extracted {len(relations)} relations: {dict(sorted(relation_types.items()))}")
    print(f"Entities: {entities_path.relative_to(PROJECT_ROOT)}")
    print(f"Relations: {relations_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

