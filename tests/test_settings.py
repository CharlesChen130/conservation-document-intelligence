from __future__ import annotations

import os

from src.conservation_intelligence.settings import load_environment, load_settings


def test_default_settings_are_consistent():
    settings = load_settings()

    assert settings.chunking.min_words <= settings.chunking.target_words
    assert settings.chunking.target_words <= settings.chunking.max_words
    assert settings.chunking.overlap_words < settings.chunking.min_words
    assert settings.retrieval.candidate_k >= settings.retrieval.top_k


def test_load_environment_reads_dotenv_without_overriding_exports(tmp_path, monkeypatch):
    dotenv_path = tmp_path / ".env"
    dotenv_path.write_text(
        "CDIP_TEST_FROM_DOTENV=loaded\nCDIP_TEST_EXPORTED=from-file\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("CDIP_TEST_FROM_DOTENV", raising=False)
    monkeypatch.setenv("CDIP_TEST_EXPORTED", "from-shell")

    assert load_environment(dotenv_path) is True
    assert os.environ["CDIP_TEST_FROM_DOTENV"] == "loaded"
    assert os.environ["CDIP_TEST_EXPORTED"] == "from-shell"
