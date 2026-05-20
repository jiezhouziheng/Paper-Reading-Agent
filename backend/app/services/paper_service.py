from app.llm.client import LLMClient
from app.storage.file_store import FileStore


class PaperService:
    def __init__(self, llm_client: LLMClient | None = None, file_store: FileStore | None = None) -> None:
        self.llm_client = llm_client or LLMClient()
        self.file_store = file_store or FileStore()

    def analyze(self, title: str, abstract: str) -> dict[str, object]:
        self.file_store.ensure_runtime_dirs()

        summary = self.llm_client.summarize_paper(title=title, abstract=abstract)
        learning_plan = self.llm_client.create_learning_plan(title=title, abstract=abstract)

        return {
            "title": title or "未命名论文",
            "summary": summary,
            "learning_plan": learning_plan,
            "storage": {
                "papers_dir": str(self.file_store.papers_dir),
                "outputs_dir": str(self.file_store.outputs_dir),
                "indexes_dir": str(self.file_store.indexes_dir),
            },
        }
