from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .catalog import save_catalog
from .paths import PROJECT_ROOT, RAW_DIR


LOGGER = logging.getLogger(__name__)
USER_AGENT = (
    "ConservationDocumentIntelligencePrototype/0.1 "
    "(public-research-corpus; contact: local research prototype)"
)


@dataclass(frozen=True)
class AcquisitionResult:
    doc_id: str
    status: str
    local_file: str = ""
    file_type: str = ""
    resolved_url: str = ""
    checksum_sha256: str = ""
    note: str = ""


def build_session(retries: int = 3) -> requests.Session:
    retry = Retry(
        total=retries,
        connect=retries,
        read=retries,
        status=retries,
        backoff_factor=0.7,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.5",
        }
    )
    session.mount("https://", adapter)
    return session


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def html_to_text(content: bytes, encoding: str | None = None) -> str:
    soup = BeautifulSoup(content, "html.parser", from_encoding=encoding)
    for element in soup(["script", "style", "noscript", "svg", "nav", "footer"]):
        element.decompose()
    root = soup.find("main") or soup.find("article") or soup.body or soup
    lines = [re.sub(r"\s+", " ", line).strip() for line in root.get_text("\n").splitlines()]
    return "\n\n".join(line for line in lines if line)


def _existing_file_is_valid(row: dict[str, str]) -> bool:
    local_file = row.get("local_file", "")
    expected_hash = row.get("checksum_sha256", "")
    if not local_file or not expected_hash:
        return False
    path = PROJECT_ROOT / local_file
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash


def acquire_source(
    row: dict[str, str],
    session: requests.Session,
    *,
    timeout: float = 45.0,
    force: bool = False,
    max_bytes: int = 100 * 1024 * 1024,
) -> AcquisitionResult:
    doc_id = row["doc_id"]
    if not force and _existing_file_is_valid(row):
        return AcquisitionResult(
            doc_id=doc_id,
            status="unchanged",
            local_file=row["local_file"],
            file_type=row["file_type"],
            resolved_url=row["resolved_url"],
            checksum_sha256=row["checksum_sha256"],
            note="Existing file checksum verified.",
        )

    try:
        response = session.get(row["url"], timeout=timeout, allow_redirects=True)
        response.raise_for_status()
        if "archivee-archived.html" in response.url and "publications.gc.ca" in row["url"]:
            response = session.get(
                row["url"],
                timeout=timeout,
                allow_redirects=True,
                headers={"Referer": response.url},
            )
            response.raise_for_status()
        content = response.content
        if len(content) > max_bytes:
            raise ValueError(f"response exceeds {max_bytes} bytes")
        if not content:
            raise ValueError("empty response")

        content_type = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
        is_pdf = content.startswith(b"%PDF-") or content_type == "application/pdf"
        if is_pdf:
            suffix = ".pdf"
            file_type = "pdf"
            output = content
        else:
            text = html_to_text(content, response.encoding)
            if len(text) < 200:
                raise ValueError("HTML page produced less than 200 characters of useful text")
            suffix = ".txt"
            file_type = "html_text"
            output = text.encode("utf-8")

        destination = RAW_DIR / f"{doc_id}{suffix}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(f"{destination.suffix}.part")
        temporary.write_bytes(output)
        temporary.replace(destination)

        return AcquisitionResult(
            doc_id=doc_id,
            status="downloaded",
            local_file=destination.relative_to(PROJECT_ROOT).as_posix(),
            file_type=file_type,
            resolved_url=response.url,
            checksum_sha256=sha256_bytes(output),
            note=f"HTTP {response.status_code}; content-type {content_type or 'unknown'}.",
        )
    except Exception as error:
        LOGGER.warning("Failed to acquire %s: %s", doc_id, error)
        return AcquisitionResult(doc_id=doc_id, status="failed", note=str(error))


def acquire_catalog(
    rows: list[dict[str, str]],
    selected_ids: Iterable[str] | None = None,
    *,
    timeout: float = 45.0,
    force: bool = False,
    session: requests.Session | None = None,
    catalog_path: Path | None = None,
) -> list[AcquisitionResult]:
    selected = set(selected_ids) if selected_ids is not None else None
    http = session or build_session()
    results: list[AcquisitionResult] = []
    retrieved_at = datetime.now(timezone.utc).isoformat()

    for row in rows:
        if selected is not None and row["doc_id"] not in selected:
            continue
        result = acquire_source(row, http, timeout=timeout, force=force)
        results.append(result)

        if result.status == "unchanged":
            continue

        row["download_status"] = result.status
        if result.local_file:
            row["local_file"] = result.local_file
            row["file_type"] = result.file_type
            row["resolved_url"] = result.resolved_url
            row["checksum_sha256"] = result.checksum_sha256
        row["retrieved_at"] = retrieved_at
        existing_note = row.get("notes", "").strip()
        if result.note and result.note not in existing_note:
            row["notes"] = "; ".join(part for part in (existing_note, result.note) if part)
        save_catalog(rows, catalog_path)

    return results
