from typing import Annotated

from pydantic import BaseModel, ConfigDict, model_validator
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.paper import PaperAnalysisResult, PaperQuestionAnswer
from app.services.paper_service import PaperService

router = APIRouter()


class PaperAnalyzeRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = ""
    abstract: str = ""
    markdown_body: str = ""

    @model_validator(mode="after")
    def require_paper_content(self) -> "PaperAnalyzeRequest":
        if not self.abstract and not self.markdown_body:
            raise ValueError("abstract or markdown_body is required")
        return self


class PaperQuestionRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str

    @model_validator(mode="after")
    def require_question(self) -> "PaperQuestionRequest":
        if not self.question:
            raise ValueError("question is required")
        return self

def get_paper_service() -> PaperService:
    return PaperService()

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


@router.post("/papers/analyze", response_model=PaperAnalysisResult)
def analyze_paper(
    request: PaperAnalyzeRequest,
    paper_service: Annotated[PaperService, Depends(get_paper_service)],
) -> PaperAnalysisResult:
    return paper_service.analyze(
        title=request.title,
        abstract=request.abstract,
        markdown_body=request.markdown_body,
    )


@router.post("/papers/{paper_id}/ask", response_model=PaperQuestionAnswer)
def ask_paper(
    paper_id: str,
    request: PaperQuestionRequest,
    paper_service: Annotated[PaperService, Depends(get_paper_service)],
) -> PaperQuestionAnswer:
    try:
        return paper_service.ask(paper_id=paper_id, question=request.question)
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
