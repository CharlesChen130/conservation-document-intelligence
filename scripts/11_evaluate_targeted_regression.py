"""Run selected known holdout questions with detailed one-call diagnostics."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.chatbot import OpenAIAnswerProvider, answer_question
from src.conservation_intelligence.evaluation import load_holdout_spec
from src.conservation_intelligence.paths import OUTPUTS_DIR
from src.conservation_intelligence.semantic import OpenAIEmbeddingProvider
from src.conservation_intelligence.settings import load_settings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ids",
        required=True,
        help="Comma-separated known holdout IDs, for example H04,H09,H11,H15.",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        default=PROJECT_ROOT / "data" / "holdout_spec.yaml",
        help="Holdout specification containing the requested IDs.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUTS_DIR / "targeted_regression_diagnostics.json",
        help="Separate diagnostic JSON destination.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested = [value.strip().upper() for value in args.ids.split(",") if value.strip()]
    spec_path = args.spec if args.spec.is_absolute() else PROJECT_ROOT / args.spec
    spec = load_holdout_spec(spec_path)
    by_id = {item["id"]: item for item in spec["questions"]}
    unknown = [value for value in requested if value not in by_id]
    if unknown:
        raise ValueError(f"Unknown holdout IDs: {', '.join(unknown)}")

    load_dotenv(PROJECT_ROOT / ".env")
    settings = load_settings()
    provider = OpenAIAnswerProvider(
        model=os.getenv("OPENAI_CHAT_MODEL") or settings.models.chat,
        max_output_tokens=settings.chatbot.max_output_tokens,
    )
    embedding_provider = OpenAIEmbeddingProvider(
        model=os.getenv("OPENAI_EMBEDDING_MODEL") or settings.models.embedding,
    )
    records: list[dict[str, object]] = []
    output_path = (
        args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    )

    for item_id in requested:
        item = by_id[item_id]
        provider.last_response_status = ""
        provider.last_incomplete_reason = ""
        provider.last_grounding_errors = ()
        input_before = provider.input_tokens_used
        output_before = provider.output_tokens_used
        embedding_before = embedding_provider.input_tokens_used
        started = perf_counter()
        result = answer_question(
            item["question"],
            provider,
            embedding_provider=embedding_provider,
            top_k=settings.chatbot.top_k,
            candidate_k=settings.retrieval.candidate_k,
        )
        elapsed = perf_counter() - started
        record = {
            "id": item_id,
            "question": item["question"],
            "expected_behavior": item["expected_behavior"],
            "evaluation_focus": item["evaluation_focus"],
            "status": result.generation_status,
            "answer": result.answer,
            "evidence_chunk_ids": [value.chunk_id for value in result.evidence],
            "elapsed_seconds": round(elapsed, 3),
            "embedding_input_tokens": embedding_provider.input_tokens_used - embedding_before,
            "chat_input_tokens": provider.input_tokens_used - input_before,
            "chat_output_tokens": provider.output_tokens_used - output_before,
            "response_status": provider.last_response_status,
            "incomplete_reason": provider.last_incomplete_reason,
            "grounding_errors": list(provider.last_grounding_errors),
            "structured_decision": (
                asdict(provider.last_decision)
                if provider.last_decision is not None
                else None
            ),
        }
        records.append(record)
        temporary = output_path.with_suffix(".json.part")
        temporary.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
        temporary.replace(output_path)
        print(
            f"{item_id}: {result.generation_status}; {elapsed:.3f}s; "
            f"embedding={record['embedding_input_tokens']}; "
            f"chat={record['chat_input_tokens']}+{record['chat_output_tokens']}",
            flush=True,
        )
        print(result.answer, flush=True)

    print(f"Diagnostics: {output_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
