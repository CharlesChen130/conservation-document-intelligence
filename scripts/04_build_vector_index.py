from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.semantic import OpenAIEmbeddingProvider, build_faiss_index
from src.conservation_intelligence.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the persisted FAISS semantic index.")
    parser.add_argument("--model", help="Override the configured embedding model.")
    parser.add_argument("--batch-size", type=int, default=64)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv(PROJECT_ROOT / ".env")
    settings = load_settings()
    model = args.model or os.getenv("OPENAI_EMBEDDING_MODEL") or settings.models.embedding
    provider = OpenAIEmbeddingProvider(model=model)
    manifest = build_faiss_index(provider, batch_size=args.batch_size)
    print(
        f"Built semantic index: {manifest['chunk_count']} chunks, "
        f"{manifest['dimension']} dimensions, model={manifest['model']}"
    )


if __name__ == "__main__":
    main()

