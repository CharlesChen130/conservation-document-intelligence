from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.wiki import generate_wiki, validate_wiki_page


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate evidence-backed Markdown wiki pages.")
    parser.add_argument("--per-category", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pages = generate_wiki(per_category=args.per_category)
    failures = {
        page.file_path: validate_wiki_page(page.content)
        for page in pages
        if validate_wiki_page(page.content)
    }
    for page in pages:
        print(f"{page.title}: {page.file_path}")
    if failures:
        details = "; ".join(f"{path}: {errors}" for path, errors in failures.items())
        raise SystemExit(f"Wiki validation failed: {details}")
    print(f"Generated and validated {len(pages)} wiki pages.")


if __name__ == "__main__":
    main()

