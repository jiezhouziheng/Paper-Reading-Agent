import pytest

from app.services.paper_service import PaperService
from app.storage.file_store import FileStore


def test_analyze_creates_workspace_and_files(tmp_path, fake_llm_client):
    file_store = FileStore(root_dir=tmp_path)
    service = PaperService(file_store=file_store, llm_client=fake_llm_client)

    result = service.analyze(
        title="Attention Is All You Need",
        abstract="Transformer paper abstract.",
        markdown_body="# Introduction\nTransformer body.",
    )

    assert result.paper_id.startswith("attention-is-all-you-need-")
    assert result.title == "Attention Is All You Need"
    assert result.source.type == "markdown"
    assert result.source.markdown_body_chars > 0

    analysis_json = tmp_path / "outputs" / result.paper_id / "analysis.json"
    reading_note = tmp_path / "outputs" / result.paper_id / "reading_note.md"

    assert analysis_json.exists()
    assert reading_note.exists()

    paper_markdown = tmp_path / "papers" / result.paper_id / "paper.md"

    assert paper_markdown.exists()
    assert paper_markdown.read_text(encoding="utf-8") == "# Introduction\nTransformer body."
    assert result.source.markdown_path == str(paper_markdown)
    assert len(result.sections) == 1
    assert result.sections[0].title == "Introduction"

    note_text = reading_note.read_text(encoding="utf-8")

    assert "## 1. 基本信息" in note_text
    assert "## 3. 论文总结" in note_text
    assert "## 6. 学习计划" in note_text

    chunks_json = tmp_path / "outputs" / result.paper_id / "chunks.json"

    assert chunks_json.exists()
    assert result.artifacts.chunks_json == str(chunks_json)
    assert len(result.chunks) >= 1
    assert result.chunks[0].chunk_id == "chunk-0001"

def test_analyze_requires_abstract_or_markdown_body(tmp_path, fake_llm_client):
    service = PaperService(
        file_store=FileStore(root_dir=tmp_path),
        llm_client=fake_llm_client,
    )

    with pytest.raises(ValueError, match="abstract or markdown_body"):
        service.analyze(title="Only Title", abstract="", markdown_body="")


def test_analyze_supports_non_ascii_title(tmp_path, fake_llm_client):
    service = PaperService(
        file_store=FileStore(root_dir=tmp_path),
        llm_client=fake_llm_client,
    )

    result = service.analyze(
        title="注意力机制论文",
        abstract="这是一段中文摘要。",
        markdown_body="",
    )

    assert result.title == "注意力机制论文"
    assert result.paper_id.startswith("paper-")
    assert "untitled" not in result.paper_id