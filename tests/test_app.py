from __future__ import annotations

from streamlit.testing.v1 import AppTest

from src.conservation_intelligence.paths import PROJECT_ROOT


def test_streamlit_shell_renders_required_tabs():
    app = AppTest.from_file(PROJECT_ROOT / "app.py")

    app.run(timeout=10)

    assert not app.exception
    assert [tab.label for tab in app.tabs] == [
        "Corpus",
        "Search",
        "Wiki",
        "Chatbot",
        "Evaluation",
    ]

