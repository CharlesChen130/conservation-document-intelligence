from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = PROJECT_ROOT / "config.yaml"
DATA_DIR = PROJECT_ROOT / "data"
METADATA_PATH = DATA_DIR / "metadata.csv"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DB_DIR = PROJECT_ROOT / "db"
DATABASE_PATH = DB_DIR / "conservation.db"
VECTOR_INDEX_DIR = PROJECT_ROOT / "vector_index"
FAISS_INDEX_PATH = VECTOR_INDEX_DIR / "chunks.faiss"
FAISS_MANIFEST_PATH = VECTOR_INDEX_DIR / "manifest.json"
WIKI_DIR = PROJECT_ROOT / "wiki"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

REQUIRED_DIRECTORIES = (
    RAW_DIR,
    PROCESSED_DIR,
    DB_DIR,
    VECTOR_INDEX_DIR,
    WIKI_DIR / "species",
    WIKI_DIR / "habitats",
    WIKI_DIR / "locations",
    WIKI_DIR / "threats",
    WIKI_DIR / "agencies",
    OUTPUTS_DIR,
)


def ensure_directories() -> None:
    """Create the project directories that hold source and generated artifacts."""
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
