import pytest
from fastapi.testclient import TestClient

from app.api.routes import get_paper_service
from app.main import app
from app.services.paper_service import PaperService
from app.storage.file_store import FileStore

# API 测试仍然测试 FastAPI 路由，但服务层里的 LLM 被替换成 fake，不会读真实 .env
@pytest.fixture
def client(tmp_path, fake_llm_client):
    def override_paper_service():
        return PaperService(
            file_store=FileStore(root_dir=tmp_path),
            llm_client=fake_llm_client,
        )

    app.dependency_overrides[get_paper_service] = override_paper_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "Paper-Reading-Agent",
    }


def test_analyze_paper_api(client):
    response = client.post(
        "/api/papers/analyze",
        json={
            "title": "Attention Is All You Need",
            "abstract": "Transformer paper abstract.",
            "markdown_body": "# Introduction\nTransformer body.",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["paper_id"].startswith("attention-is-all-you-need-")
    assert data["title"] == "Attention Is All You Need"
    assert data["source"]["markdown_path"]
    assert data["sections"][0]["title"] == "Introduction"
    assert data["artifacts"]["chunks_json"]
    assert len(data["chunks"]) >= 1
    assert data["chunks"][0]["chunk_id"] == "chunk-0001"
    assert "summary" in data
    assert "learning_plan" in data
    assert "glossary" in data
    assert "artifacts" in data


def test_analyze_paper_requires_content(client):
    response = client.post(
        "/api/papers/analyze",
        json={"title": "Only Title"},
    )

    assert response.status_code == 422


def test_ask_paper_api(client):
    analyze_response = client.post(
        "/api/papers/analyze",
        json={
            "title": "Attention Paper",
            "abstract": "Transformer abstract.",
            "markdown_body": "# Method\nAttention computes weighted token representations.",
        },
    )

    paper_id = analyze_response.json()["paper_id"]

    response = client.post(
        f"/api/papers/{paper_id}/ask",
        json={"question": "How does attention work?"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["paper_id"] == paper_id
    assert data["citations"]
    assert data["citations"][0]["chunk_id"] == "chunk-0001"


def test_ask_paper_returns_404_for_missing_chunks(client):
    response = client.post(
        "/api/papers/missing-paper/ask",
        json={"question": "What is this paper about?"},
    )

    assert response.status_code == 404