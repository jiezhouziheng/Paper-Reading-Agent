from datetime import datetime ## 生成时间
import re ## 清理标题

from app.llm.client import LLMClient
from app.storage.file_store import FileStore


class PaperService:
    def __init__(self, llm_client: LLMClient | None = None, file_store: FileStore | None = None) -> None:
        self.llm_client = llm_client or LLMClient()
        self.file_store = file_store or FileStore()

    def _create_paper_id(self, title: str) -> str:
        base = title.strip().lower() or "untitled-paper"
        base = re.sub(r"[^a-z0-9]+", "-", base)
        base = base.strip("-") or "untitled-paper"

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{base}-{timestamp}"

    def analyze(self, title: str, abstract: str, markdown_body: str = "") -> dict[str, object]:
        paper_id = self._create_paper_id(title)
        workspace = self.file_store.prepare_paper_workspace(paper_id)

        summary = self.llm_client.summarize_paper(title=title, abstract=abstract)
        learning_plan = self.llm_client.create_learning_plan(title=title, abstract=abstract)
        glossary = self.llm_client.extract_glossary(title=title, abstract=abstract)

        analysis_json_path = workspace["output_dir"] / "analysis.json"
        reading_note_path = workspace["output_dir"] / "reading_note.md"

        result = {
            "paper_id": paper_id,
            "title": title or "未命名论文",
            "source": {
                "type": "markdown" if markdown_body else "abstract_only",
                "markdown_body_chars": len(markdown_body),
            },
            "summary": summary,
            "learning_plan": learning_plan,
            "glossary": glossary,
            "qa": [],
            "artifacts": {
                "paper_dir": str(workspace["paper_dir"]),
                "output_dir": str(workspace["output_dir"]),
                "analysis_json": str(analysis_json_path),
                "reading_note": str(reading_note_path),
            },
            "storage": {
                "papers_dir": str(self.file_store.papers_dir),
                "outputs_dir": str(self.file_store.outputs_dir),
                "indexes_dir": str(self.file_store.indexes_dir),
            },
        }

        self.file_store.save_json(analysis_json_path, result)
        self.file_store.save_text(
            reading_note_path,
            f"# {title or '未命名论文'}\n\n## 摘要\n{abstract or '无摘要'}\n",
        )

        return result
