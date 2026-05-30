import pytest


class FakeLLMClient:
    def analyze_paper(self, title: str, abstract: str, markdown_body: str = "") -> dict:
        return {
            "summary": {
                "research_problem": "fake research problem",
                "method": "fake method",
                "contribution": "fake contribution",
                "limitation": "fake limitation",
            },
            "learning_plan": [
                {
                    "stage": "fake stage",
                    "task": "fake task",
                }
            ],
            "glossary": [
                {
                    "term": "fake term",
                    "explanation": "fake explanation",
                }
            ],
        }


@pytest.fixture
def fake_llm_client() -> FakeLLMClient:
    return FakeLLMClient()