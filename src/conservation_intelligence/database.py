from __future__ import annotations

import sqlite3
from pathlib import Path

from .paths import DATABASE_PATH


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS documents (
    doc_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    year TEXT,
    agency TEXT,
    topic TEXT,
    url TEXT NOT NULL,
    local_file TEXT,
    file_type TEXT,
    original_url TEXT,
    resolved_url TEXT,
    download_status TEXT,
    notes TEXT,
    checksum_sha256 TEXT,
    retrieved_at TEXT
);

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL,
    page TEXT,
    chunk_text TEXT NOT NULL,
    source_url TEXT NOT NULL,
    title TEXT,
    word_count INTEGER,
    content_hash TEXT,
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entities (
    entity_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    normalized_name TEXT,
    entity_type TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    confidence REAL,
    evidence TEXT,
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE,
    FOREIGN KEY (chunk_id) REFERENCES chunks(chunk_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS relations (
    relation_id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    relation TEXT NOT NULL,
    object TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    chunk_id TEXT NOT NULL,
    evidence TEXT NOT NULL,
    confidence REAL,
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id) ON DELETE CASCADE,
    FOREIGN KEY (chunk_id) REFERENCES chunks(chunk_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS wiki_pages (
    page_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    stage TEXT NOT NULL,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,
    details TEXT
);

CREATE INDEX IF NOT EXISTS idx_chunks_doc_id ON chunks(doc_id);
CREATE INDEX IF NOT EXISTS idx_entities_doc_id ON entities(doc_id);
CREATE INDEX IF NOT EXISTS idx_entities_chunk_id ON entities(chunk_id);
CREATE INDEX IF NOT EXISTS idx_entities_type_name ON entities(entity_type, normalized_name);
CREATE INDEX IF NOT EXISTS idx_relations_doc_id ON relations(doc_id);
CREATE INDEX IF NOT EXISTS idx_relations_chunk_id ON relations(chunk_id);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    chunk_id UNINDEXED,
    title,
    chunk_text,
    tokenize = 'porter unicode61'
);
"""


def connect_database(path: Path | None = None) -> sqlite3.Connection:
    database_path = path or DATABASE_PATH
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(path: Path | None = None) -> Path:
    database_path = path or DATABASE_PATH
    with connect_database(database_path) as connection:
        connection.executescript(SCHEMA_SQL)
    return database_path

