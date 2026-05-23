from uuid import uuid4
from datetime import datetime ## 生成时间
import re ## 正则表达式模块，用于匹配 md 标题

from app.llm.client import LLMClient
from app.storage.file_store import FileStore
from app.schemas.paper import AnswerCitation, PaperAnalysisResult, PaperQuestionAnswer, TextChunk
from app.parsers.markdown_parser import parse_markdown_sections
from app.parsers.chunking import build_text_chunks
from app.renderers.reading_note import render_reading_note
from app.retrieval.keyword_retriever import KeywordRetriever


class PaperService:
    def __init__(
            self,
            llm_client: LLMClient | None = None,
            file_store: FileStore | None = None,
            retriever: KeywordRetriever | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.file_store = file_store or FileStore()
        self.retriever = retriever or KeywordRetriever()

    def _create_paper_id(self, title: str) -> str:
        base = title.strip().lower()
        base = re.sub(r"[^a-z0-9]+", "-", base)
        base = base.strip("-") or "paper"

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        unique_suffix = uuid4().hex[:8]
        return f"{base}-{timestamp}-{unique_suffix}"

    def analyze(self, title: str, abstract: str, markdown_body: str = "") -> PaperAnalysisResult:
        # 输入归一化和兜底校验
        title = (title or "").strip()
        abstract = (abstract or "").strip()
        markdown_body = (markdown_body or "").strip()

        if not abstract and not markdown_body:
            raise ValueError("abstract or markdown_body is required")

        # 正式工作
        paper_id = self._create_paper_id(title)
        workspace = self.file_store.prepare_paper_workspace(paper_id)

        markdown_path = None
        sections = []

        if markdown_body:
            markdown_path = workspace["paper_dir"] / "paper.md"
            self.file_store.save_text(markdown_path, markdown_body)
            sections = parse_markdown_sections(markdown_body)

        chunks = build_text_chunks(markdown_body, sections) if markdown_body else []
        summary = self.llm_client.summarize_paper(title=title, abstract=abstract)
        learning_plan = self.llm_client.create_learning_plan(title=title, abstract=abstract)
        glossary = self.llm_client.extract_glossary(title=title, abstract=abstract)

        analysis_json_path = workspace["output_dir"] / "analysis.json"
        reading_note_path = workspace["output_dir"] / "reading_note.md"
        chunks_json_path = workspace["output_dir"] / "chunks.json"

        result = {
            "paper_id": paper_id,
            "title": title or "未命名论文",
            "source": {
                "type": "markdown" if markdown_body else "abstract_only",
                "markdown_body_chars": len(markdown_body),
                "markdown_path": str(markdown_path) if markdown_path else None,
            },
            "sections": sections,
            "chunks": chunks,
            "summary": summary,
            "learning_plan": learning_plan,
            "glossary": glossary,
            "qa": [],
            "artifacts": {
                "paper_dir": str(workspace["paper_dir"]),
                "output_dir": str(workspace["output_dir"]),
                "analysis_json": str(analysis_json_path),
                "reading_note": str(reading_note_path),
                "chunks_json": str(chunks_json_path) if chunks else None,
            },
            "storage": {
                "papers_dir": str(self.file_store.papers_dir),
                "outputs_dir": str(self.file_store.outputs_dir),
                "indexes_dir": str(self.file_store.indexes_dir),
            },
        }

        analysis = PaperAnalysisResult(**result)

        self.file_store.save_json(analysis_json_path, analysis.model_dump(mode="json"))
        if chunks:
            self.file_store.save_json(
                chunks_json_path,
                {"paper_id": paper_id, "chunks": [chunk.model_dump(mode="json") for chunk in chunks]},
            )

        self.file_store.save_text(
            reading_note_path,
            render_reading_note(analysis=analysis, abstract=abstract),
        )

        return analysis

    def ask(self, paper_id: str, question: str) -> PaperQuestionAnswer:
        paper_id = paper_id.strip()
        question = question.strip()

        if not question:
            raise ValueError("question is required")

        chunks_json_path = self.file_store.outputs_dir / paper_id / "chunks.json"

        if not chunks_json_path.exists():
            raise FileNotFoundError(f"chunks not found for paper_id: {paper_id}")

        chunks_data = self.file_store.load_json(chunks_json_path)
        chunks = [TextChunk(**item) for item in chunks_data.get("chunks", [])]

        citations = self.retriever.retrieve(question=question, chunks=chunks)

        if not citations:
            answer = "没有在论文片段中找到与问题明显相关的内容。"
        else:
            answer = "根据当前检索到的论文片段，相关内容主要集中在：" + "、".join(
                citation.section_title for citation in citations
            )

        return PaperQuestionAnswer(
            paper_id=paper_id,
            question=question,
            answer=answer,
            citations=citations,
        )

