from __future__ import annotations

from src.conservation_intelligence.extraction import extract_source, normalize_text


def test_normalize_text_removes_noise_without_flattening_paragraphs():
    value = "Wetlands\u00a0 need\tcare.\r\n\r\n\r\n Rivers do too.\x00"

    assert normalize_text(value) == "Wetlands need care.\n\nRivers do too."


def test_extract_text_source(tmp_path):
    raw_dir = tmp_path / "data" / "raw"
    processed_dir = tmp_path / "data" / "processed"
    raw_dir.mkdir(parents=True)
    source = raw_dir / "DOC999.txt"
    source.write_text("Wetland restoration evidence. " * 30, encoding="utf-8")
    row = {
        "doc_id": "DOC999",
        "local_file": "data/raw/DOC999.txt",
        "file_type": "html_text",
        "extracted_file": "",
        "extraction_status": "",
    }

    result = extract_source(row, project_root=tmp_path, processed_dir=processed_dir)

    assert result.status == "extracted"
    assert result.page_count == 1
    assert result.character_count > 500
    output = (tmp_path / result.extracted_file).read_text(encoding="utf-8")
    assert output.startswith("--- Source Text ---")
    assert "Wetland restoration evidence." in output

