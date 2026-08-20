from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from .paths import CONFIG_PATH, PROJECT_ROOT


@dataclass(frozen=True)
class ChunkingSettings:
    target_words: int
    min_words: int
    max_words: int
    overlap_words: int


@dataclass(frozen=True)
class RetrievalSettings:
    backend: str
    top_k: int
    candidate_k: int


@dataclass(frozen=True)
class ModelSettings:
    chat: str
    embedding: str


@dataclass(frozen=True)
class ChatbotSettings:
    top_k: int
    max_question_characters: int
    max_output_tokens: int


@dataclass(frozen=True)
class Settings:
    title: str
    disclaimer: str
    chunking: ChunkingSettings
    retrieval: RetrievalSettings
    models: ModelSettings
    chatbot: ChatbotSettings


def load_environment(path: Path | None = None) -> bool:
    """Load local runtime settings without overriding exported environment values."""
    return load_dotenv(path or PROJECT_ROOT / ".env", override=False)


def _section(data: dict[str, Any], name: str) -> dict[str, Any]:
    value = data.get(name)
    if not isinstance(value, dict):
        raise ValueError(f"Missing or invalid '{name}' section in configuration")
    return value


def load_settings(path: Path | None = None) -> Settings:
    config_path = path or CONFIG_PATH
    with config_path.open("r", encoding="utf-8") as config_file:
        data = yaml.safe_load(config_file) or {}

    app = _section(data, "app")
    chunking = ChunkingSettings(**_section(data, "chunking"))
    retrieval = RetrievalSettings(**_section(data, "retrieval"))
    models = ModelSettings(**_section(data, "models"))
    chatbot = ChatbotSettings(**_section(data, "chatbot"))

    if not 0 <= chunking.overlap_words < chunking.min_words:
        raise ValueError("chunk overlap must be non-negative and smaller than min_words")
    if not chunking.min_words <= chunking.target_words <= chunking.max_words:
        raise ValueError("target_words must be between min_words and max_words")
    if retrieval.top_k <= 0 or retrieval.candidate_k < retrieval.top_k:
        raise ValueError("retrieval candidate_k must be greater than or equal to top_k")
    if min(
        chatbot.top_k,
        chatbot.max_question_characters,
        chatbot.max_output_tokens,
    ) <= 0:
        raise ValueError("chatbot limits must be positive")

    return Settings(
        title=str(app["title"]),
        disclaimer=str(app["disclaimer"]),
        chunking=chunking,
        retrieval=retrieval,
        models=models,
        chatbot=chatbot,
    )
