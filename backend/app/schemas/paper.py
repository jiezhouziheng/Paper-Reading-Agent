from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SourceInfo(BaseModel):
    type: str
    markdown_body_chars: int
    markdown_path: str | None = None


class MarkdownSection(BaseModel):
    order: int
    title: str
    level: int
    char_count: int


class Summary(BaseModel):
    research_problem: str
    method: str
    contribution: str
    limitation: str


class LearningTask(BaseModel):
    stage: str
    task: str


class GlossaryItem(BaseModel):
    term: str
    explanation: str


class TextChunk(BaseModel):
    chunk_id: str
    section_title: str
    section_level: int
    order: int
    text: str
    char_count: int


class ArtifactPaths(BaseModel):
    paper_dir: str
    output_dir: str
    analysis_json: str
    reading_note: str
    chunks_json: str | None = None


class StoragePaths(BaseModel):
    papers_dir: str
    outputs_dir: str
    indexes_dir: str


class PaperAnalysisResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    paper_id: str
    title: str
    source: SourceInfo
    sections: list[MarkdownSection] = Field(default_factory=list)
    chunks: list[TextChunk] = Field(default_factory=list)
    summary: Summary
    learning_plan: list[LearningTask]
    glossary: list[GlossaryItem]
    qa: list[dict[str, Any]] = Field(default_factory=list)
    artifacts: ArtifactPaths
    storage: StoragePaths


class AnswerCitation(BaseModel):
    chunk_id: str
    section_title: str
    text: str
    score: int


class PaperQuestionAnswer(BaseModel):
    paper_id: str
    question: str
    answer: str
    citations: list[AnswerCitation] = Field(default_factory=list)

