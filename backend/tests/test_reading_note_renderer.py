from app.renderers.reading_note import render_reading_note
from app.services.paper_service import PaperService
from app.storage.file_store import FileStore


def test_render_reading_note_contains_stable_sections(tmp_path):
    service = PaperService(file_store=FileStore(root_dir=tmp_path))

    analysis = service.analyze(
        title="Attention Is All You Need",
        abstract="Transformer paper abstract.",
        markdown_body="# Introduction\nTransformer body.",
    )

    note = render_reading_note(
        analysis=analysis,
        abstract="Transformer paper abstract.",
    )

    assert "# Attention Is All You Need" in note
    assert "## 1. 基本信息" in note
    assert "## 3. 论文总结" in note
    assert "## 4. 章节结构" in note
    assert "## 5. 术语表" in note
    assert "## 6. 学习计划" in note
    assert "Introduction" in note
    assert "Transformer paper abstract." in note
