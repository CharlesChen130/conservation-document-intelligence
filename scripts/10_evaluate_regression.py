"""Replay the known holdout questions as a post-repair regression diagnostic.

This intentionally writes a separate artifact. It never overwrites the immutable
first-run holdout answer report.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, replace
from pathlib import Path
from time import perf_counter

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
from src.conservation_intelligence.paths import OUTPUTS_DIR
from src.conservation_intelligence.semantic import OpenAIEmbeddingProvider
from src.conservation_intelligence.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replay the known holdout as a post-repair regression set."
    )
    parser.add_argument(
        "--with-openai",
        action="store_true",
        help="Use live OpenAI retrieval and grounded answer generation.",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=PROJECT_ROOT / "data" / "holdout_spec.yaml",
        help="Known holdout specification to replay.",
    )
    parser.add_argument(
        "--artifact-prefix",
        default="holdout_regression",
        help="Output filename prefix under outputs/.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv(PROJECT_ROOT / ".env")
    settings = load_settings()
    spec_path = args.spec if args.spec.is_absolute() else PROJECT_ROOT / args.spec
    spec = load_holdout_spec(spec_path)
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
    records = []
    metrics = []
    output_path = OUTPUTS_DIR / f"{args.artifact_prefix}_answers.md"
    checkpoint_path = OUTPUTS_DIR / f"{args.artifact_prefix}_checkpoint.json"
    metrics_path = OUTPUTS_DIR / f"{args.artifact_prefix}_metrics.json"
    for number, item in enumerate(spec["questions"], start=1):
        if provider is not None:
            provider.last_response_status = ""
            provider.last_incomplete_reason = ""
            provider.last_grounding_errors = ()
        chat_input_before = getattr(provider, "input_tokens_used", 0)
        chat_output_before = getattr(provider, "output_tokens_used", 0)
        embedding_input_before = getattr(embedding_provider, "input_tokens_used", 0)
        started = perf_counter()
        record = evaluate_questions(
            [item["question"]],
            provider=provider,
            embedding_provider=embedding_provider,
            top_k=settings.chatbot.top_k,
            candidate_k=settings.retrieval.candidate_k,
        )[0]
        elapsed_seconds = perf_counter() - started
        metric = {
            "number": number,
            "id": item["id"],
            "elapsed_seconds": round(elapsed_seconds, 3),
            "embedding_input_tokens": (
                getattr(embedding_provider, "input_tokens_used", 0)
                - embedding_input_before
            ),
            "chat_input_tokens": (
                getattr(provider, "input_tokens_used", 0) - chat_input_before
            ),
            "chat_output_tokens": (
                getattr(provider, "output_tokens_used", 0) - chat_output_before
            ),
            "response_status": getattr(provider, "last_response_status", ""),
            "incomplete_reason": getattr(provider, "last_incomplete_reason", ""),
            "grounding_errors": list(
                getattr(provider, "last_grounding_errors", ())
            ),
        }
        metrics.append(metric)
        records.append(replace(record, number=number))
        checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_checkpoint = checkpoint_path.with_suffix(".json.part")
        temporary_checkpoint.write_text(
            json.dumps([asdict(value) for value in records], indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_checkpoint.replace(checkpoint_path)
        temporary_metrics = metrics_path.with_suffix(".json.part")
        temporary_metrics.write_text(
            json.dumps(metrics, indent=2) + "\n",
            encoding="utf-8",
        )
        temporary_metrics.replace(metrics_path)
        print(
            f"[{number:02d}/{len(spec['questions'])}] {item['id']}: "
            f"{record.status}; {metric['elapsed_seconds']:.3f}s; "
            f"embedding={metric['embedding_input_tokens']} tokens; "
            f"chat={metric['chat_input_tokens']}+{metric['chat_output_tokens']} tokens",
            flush=True,
        )
    write_holdout_report(
        records,
        output_path=output_path,
        spec_path=spec_path,
        provider_model=provider.model if provider is not None else None,
    )
    counts: dict[str, int] = {}
    for record in records:
        counts[record.status] = counts.get(record.status, 0) + 1
    print(f"Replayed known holdout as regression: {dict(sorted(counts.items()))}")
    print(
        "Usage: "
        f"{sum(value['embedding_input_tokens'] for value in metrics)} embedding input, "
        f"{sum(value['chat_input_tokens'] for value in metrics)} chat input, "
        f"{sum(value['chat_output_tokens'] for value in metrics)} chat output tokens; "
        f"{sum(value['elapsed_seconds'] for value in metrics):.3f}s cumulative"
    )
    print(f"Report: {output_path.relative_to(PROJECT_ROOT)}")
    print(f"Metrics: {metrics_path.relative_to(PROJECT_ROOT)}")
    print("Immutable first-run holdout artifacts were not modified.")


if __name__ == "__main__":
    main()
