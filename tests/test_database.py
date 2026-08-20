from __future__ import annotations

from src.conservation_intelligence.database import connect_database, initialize_database


def test_initialize_database_is_idempotent(tmp_path):
    database_path = tmp_path / "test.db"

    initialize_database(database_path)
    initialize_database(database_path)

    with connect_database(database_path) as connection:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type IN ('table', 'view')"
            )
        }

    assert {"documents", "chunks", "entities", "relations", "wiki_pages"} <= tables
    assert "chunks_fts" in tables


def test_foreign_keys_are_enforced(tmp_path):
    database_path = tmp_path / "test.db"
    initialize_database(database_path)

    with connect_database(database_path) as connection:
        enabled = connection.execute("PRAGMA foreign_keys").fetchone()[0]

    assert enabled == 1

