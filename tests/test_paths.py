from __future__ import annotations

from src.conservation_intelligence.paths import PROJECT_ROOT


def test_project_root_contains_requirements_documents():
    assert (PROJECT_ROOT / "Document_Intelligence_Project_Description.docx").exists()
    assert (PROJECT_ROOT / "Hugging_Face_Spaces_Deployment_Guide_Conservation_Prototype.docx").exists()

