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
