import pytest

from app.services.paper_service import PaperService
from app.storage.file_store import FileStore


def test_ask_returns_relevant_citations(tmp_path):
    service = PaperService(file_store=FileStore(root_dir=tmp_path))

    analysis = service.analyze(
        title="Attention Paper",
        abstract="Transformer abstract.",
        markdown_body="# Method\nAttention computes weighted token representations.",
    )

    answer = service.ask(
        paper_id=analysis.paper_id,
        question="How does attention work?",
    )

    assert answer.paper_id == analysis.paper_id
    assert answer.question == "How does attention work?"
    assert answer.citations
    assert answer.citations[0].chunk_id == "chunk-0001"
    assert "Attention" in answer.citations[0].text


def test_ask_requires_question(tmp_path):
    service = PaperService(file_store=FileStore(root_dir=tmp_path))

    with pytest.raises(ValueError, match="question is required"):
        service.ask(paper_id="missing", question="")
