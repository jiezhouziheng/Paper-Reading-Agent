from pydantic import BaseModel
from fastapi import APIRouter

from app.services.paper_service import PaperService

router = APIRouter()
paper_service = PaperService()


class PaperAnalyzeRequest(BaseModel):
    title: str = ""
    abstract: str = ""
    markdown_body: str = ""


@router.get("/modules")
def list_modules() -> dict[str, list[str]]:
    return {
        "modules": [
            "frontend",
            "backend",
            "llm",
            "storage",
        ]
    }


@router.post("/papers/analyze")
def analyze_paper(request: PaperAnalyzeRequest) -> dict[str, object]:
    return paper_service.analyze(
        title=request.title,
        abstract=request.abstract,
        markdown_body=request.markdown_body,
    )