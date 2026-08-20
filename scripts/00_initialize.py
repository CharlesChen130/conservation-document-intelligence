from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conservation_intelligence.database import initialize_database
from src.conservation_intelligence.paths import ensure_directories
from src.conservation_intelligence.settings import load_settings


def main() -> None:
    ensure_directories()
    settings = load_settings()
    database_path = initialize_database()
    print(f"Initialized {settings.title}")
    print(f"Database: {database_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

