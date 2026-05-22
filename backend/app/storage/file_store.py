import json

from pathlib import Path


class FileStore:
    def __init__(self, root_dir: str | Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[3]
        self.root_dir = Path(root_dir) if root_dir is not None else project_root / "data"
        self.papers_dir = self.root_dir / "papers"
        self.outputs_dir = self.root_dir / "outputs"
        self.indexes_dir = self.root_dir / "indexes"

    def ensure_runtime_dirs(self) -> None:
        self.papers_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        self.indexes_dir.mkdir(parents=True, exist_ok=True)

    def prepare_paper_workspace(self, paper_id: str) -> dict[str, Path]:
        self.ensure_runtime_dirs()

        paper_dir = self.papers_dir / paper_id
        output_dir = self.outputs_dir / paper_id

        paper_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)

        return {
            "paper_dir": paper_dir,
            "output_dir": output_dir,
        }

    def save_json(self, path: Path, data: dict) -> None:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def save_text(self, path: Path, text: str) -> None:
        path.write_text(text, encoding="utf-8")

    def load_json(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))
