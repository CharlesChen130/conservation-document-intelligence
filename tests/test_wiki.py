from __future__ import annotations

from src.conservation_intelligence.chunking import Chunk
from src.conservation_intelligence.database import connect_database, initialize_database
from src.conservation_intelligence.entity_extraction import (
    EntityMention,
    RelationMention,
    replace_extractions,
)
from src.conservation_intelligence.repository import replace_document_chunks, sync_documents
from src.conservation_intelligence.wiki import generate_wiki, slugify, validate_wiki_page


def test_slug_and_page_validation():
    assert slugify("U.S. Fish & Wildlife Service") == "u-s-fish-and-wildlife-service"
    assert validate_wiki_page("No structured page")


def test_generate_evidence_backed_wiki_page(tmp_path):
    database_path = tmp_path / "test.db"
    wiki_dir = tmp_path / "wiki"
    initialize_database(database_path)
    document = {
        "doc_id": "DOC999",
        "title": "Wetland Plan",
        "year": "2026",
        "agency": "Test Agency",
        "topic": "Wetlands",
        "url": "https://example.org/wetland",
        "local_file": "data/raw/DOC999.txt",
        "file_type": "html_text",
        "original_url": "https://example.org/wetland",
        "resolved_url": "https://example.org/wetland",
        "download_status": "downloaded",
        "notes": "",
        "checksum_sha256": "abc",
        "retrieved_at": "2026-01-01T00:00:00+00:00",
    }
    chunk = Chunk(
        "DOC999-C0001",
        "DOC999",
        "4",
        "Wetlands provide habitat and improve water quality.",
        7,
        "hash",
    )
    noisy_chunk = Chunk(
        "DOC999-C0002",
        "DOC999",
        "5",
        "TABLE OF CONTENTS Wetland ........ 4 Literature Cited ........ 9",
        10,
        "noise-hash",
    )
    second_chunk = Chunk(
        "DOC999-C0003",
        "DOC999",
        "6",
        "Mallards use wetlands for feeding and seasonal shelter.",
        8,
        "second-hash",
    )
    wetland = EntityMention(
        "ENT-test",
        "Wetland",
        "wetland",
        "habitat",
        "DOC999",
        "DOC999-C0001",
        0.9,
        "Wetlands provide habitat and improve water quality.",
    )
    noisy_wetland = EntityMention(
        "ENT-noise",
        "Wetland",
        "wetland",
        "habitat",
        "DOC999",
        "DOC999-C0002",
        0.9,
        "TABLE OF CONTENTS Wetland ........ 4 Literature Cited ........ 9",
    )
    second_wetland = EntityMention(
        "ENT-wetland-second",
        "Wetland",
        "wetland",
        "habitat",
        "DOC999",
        "DOC999-C0003",
        0.9,
        "Mallards use wetlands for feeding and seasonal shelter.",
    )
    mallard = EntityMention(
        "ENT-mallard",
        "Mallard",
        "mallard",
        "species",
        "DOC999",
        "DOC999-C0001",
        0.9,
        "Wetlands provide habitat and improve water quality for Mallards.",
    )
    second_mallard = EntityMention(
        "ENT-mallard-second",
        "Mallard",
        "mallard",
        "species",
        "DOC999",
        "DOC999-C0003",
        0.9,
        "Mallards use wetlands for feeding and seasonal shelter.",
    )
    relation = RelationMention(
        "REL-test",
        "Mallard",
        "species_uses_habitat",
        "Wetland",
        "DOC999",
        "DOC999-C0001",
        "Wetlands provide habitat and improve water quality for Mallards.",
        0.9,
    )
    with connect_database(database_path) as connection:
        sync_documents(connection, [document])
        replace_document_chunks(
            connection, document, [chunk, noisy_chunk, second_chunk]
        )
        replace_extractions(
            connection,
            ["DOC999"],
            [wetland, noisy_wetland, second_wetland, mallard, second_mallard],
            [relation],
        )

    stale_page = wiki_dir / "species" / "obsolete.md"
    manual_page = wiki_dir / "species" / "manual-notes.md"
    stale_page.parent.mkdir(parents=True)
    stale_page.write_text("---\ngenerated: true\n---\n", encoding="utf-8")
    manual_page.write_text("# Manual notes\n", encoding="utf-8")

    pages = generate_wiki(
        database_path=database_path,
        wiki_dir=wiki_dir,
        per_category=1,
    )

    assert len(pages) == 2
    pages_by_title = {page.title: page for page in pages}
    wetland_page = pages_by_title["Wetland"]
    assert validate_wiki_page(wetland_page.content) == []
    assert "[DOC999, p. 4]" in wetland_page.content
    assert "TABLE OF CONTENTS" not in wetland_page.content
    assert "explicit `species_uses_habitat` relation" in wetland_page.content
    assert "../species/mallard.md" in wetland_page.content
    assert (wiki_dir / "habitats" / "wetland.md").exists()
    assert (wiki_dir / "species" / "mallard.md").exists()
    assert not stale_page.exists()
    assert manual_page.exists()


def test_validator_rejects_uncited_and_noisy_facts():
    page = """# Wetland

## Summary
Wetland summary without evidence.

## Key facts
- TABLE OF CONTENTS Wetland ........ 4

## Related documents
- **DOC999**

## Related entities
- **Mallard** (species) shares 3 evidence chunks.

## Evidence snippets
> Unattributed text.

## Open questions
- More research is needed.
"""
    errors = validate_wiki_page(page)
    assert "summary contains no corpus citation" in errors
    assert any(error.startswith("noisy key fact:") for error in errors)
    assert "page presents chunk co-occurrence as a relationship" in errors
    assert any(error.startswith("unattributed evidence snippet:") for error in errors)
    assert any(error.startswith("open question is not a question:") for error in errors)
