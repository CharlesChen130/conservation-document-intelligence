from __future__ import annotations

from src.conservation_intelligence import acquisition
from src.conservation_intelligence.acquisition import acquire_source, html_to_text, sha256_bytes


def test_html_to_text_removes_navigation_and_scripts():
    html = b"""
    <html><body>
      <nav>Menu that should be removed</nav>
      <main><h1>Wetland plan</h1><p>Wetland restoration evidence.</p></main>
      <script>alert('remove me')</script>
    </body></html>
    """

    text = html_to_text(html)

    assert "Wetland plan" in text
    assert "Wetland restoration evidence" in text
    assert "Menu" not in text
    assert "alert" not in text


def test_sha256_bytes_is_stable():
    assert sha256_bytes(b"conservation") == sha256_bytes(b"conservation")
    assert sha256_bytes(b"conservation") != sha256_bytes(b"wetland")


def test_canada_archive_interstitial_is_retried_in_same_session(tmp_path, monkeypatch):
    class FakeResponse:
        def __init__(self, url: str, content: bytes, content_type: str):
            self.url = url
            self.content = content
            self.headers = {"Content-Type": content_type}
            self.encoding = "utf-8"
            self.status_code = 200

        def raise_for_status(self):
            return None

    class FakeSession:
        def __init__(self):
            self.calls = []

        def get(self, url, **kwargs):
            self.calls.append((url, kwargs))
            if len(self.calls) == 1:
                return FakeResponse(
                    "https://publications.gc.ca/archivee-archived.html",
                    b"<html><body>Archived notice</body></html>",
                    "text/html",
                )
            return FakeResponse(url, b"%PDF-1.7\nreport", "application/pdf")

    monkeypatch.setattr(acquisition, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(acquisition, "RAW_DIR", tmp_path / "data" / "raw")
    source_url = "https://publications.gc.ca/collections/collection_2025/report.pdf"
    session = FakeSession()

    result = acquire_source({"doc_id": "DOC014", "url": source_url}, session, force=True)

    assert result.status == "downloaded"
    assert result.file_type == "pdf"
    assert len(session.calls) == 2
    assert session.calls[1][1]["headers"]["Referer"].endswith("archivee-archived.html")
    assert (tmp_path / result.local_file).read_bytes().startswith(b"%PDF-")
