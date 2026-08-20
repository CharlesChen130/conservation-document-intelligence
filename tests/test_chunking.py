from __future__ import annotations

from src.conservation_intelligence.chunking import chunk_text, parse_page_tokens


def test_parse_page_tokens_keeps_page_numbers():
    text = "--- Page 1 ---\n\nWetland evidence here.\n\n--- Page 2 ---\n\nRiver evidence there."

    tokens = parse_page_tokens(text)

    assert tokens[0] == ("Wetland", 1)
    assert tokens[-1] == ("there.", 2)


def test_chunk_text_respects_size_and_overlap_contract():
    first_page = " ".join(f"wetland{i}" for i in range(1_000))
    second_page = " ".join(f"river{i}" for i in range(1_000))
    text = f"--- Page 1 ---\n\n{first_page}\n\n--- Page 2 ---\n\n{second_page}"

    chunks = chunk_text("DOC999", text)

    assert len(chunks) == 3
    assert all(600 <= chunk.word_count <= 900 for chunk in chunks)
    assert chunks[0].chunk_id == "DOC999-C0001"
    assert chunks[-1].page == "2"
    assert chunks[0].text.split()[-100:] == chunks[1].text.split()[:100]

