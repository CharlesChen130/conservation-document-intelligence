"""Run the frozen post-repair holdout set without changing the application."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.chatbot import OpenAIAnswerProvider
from src.conservation_intelligence.evaluation import (
    evaluate_questions,
    load_holdout_spec,
    write_holdout_report,
)
from src.conservation_intelligence.semantic import OpenAIEmbeddingProvider
from src.conservation_intelligence.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate the frozen 20-question holdout set."
    )
    parser.add_argument(
        "--with-openai",
        action="store_true",
        help="Generate live grounded answers in addition to retrieval results.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv(PROJECT_ROOT / ".env")
    settings = load_settings()
    spec = load_holdout_spec()
    questions = [item["question"] for item in spec["questions"]]
    provider = None
    embedding_provider = None
    if args.with_openai:
        provider = OpenAIAnswerProvider(
            model=os.getenv("OPENAI_CHAT_MODEL") or settings.models.chat,
            max_output_tokens=settings.chatbot.max_output_tokens,
        )
        embedding_provider = OpenAIEmbeddingProvider(
            model=os.getenv("OPENAI_EMBEDDING_MODEL") or settings.models.embedding,
        )
    records = evaluate_questions(
        questions,
        provider=provider,
        embedding_provider=embedding_provider,
        top_k=settings.chatbot.top_k,
        candidate_k=settings.retrieval.candidate_k,
    )
    output_path = write_holdout_report(
        records,
        provider_model=provider.model if provider is not None else None,
    )
    counts: dict[str, int] = {}
    for record in records:
        counts[record.status] = counts.get(record.status, 0) + 1
    print(f"Evaluated frozen holdout set: {dict(sorted(counts.items()))}")
    print(f"Report: {output_path.relative_to(PROJECT_ROOT)}")
    print("No application tuning was performed from these results.")


if __name__ == "__main__":
    main()
