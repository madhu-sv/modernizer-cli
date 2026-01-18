import shutil
from pathlib import Path
from rich.console import Console

console = Console()

class SandboxManager:
    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.sandbox_root = self.project_root / ".modernizer_sandbox"

    def create(self):
        if self.sandbox_root.exists():
            shutil.rmtree(self.sandbox_root)
        
        # Ignore heavy/irrelevant folders
        ignore = shutil.ignore_patterns(
            '.git', 'target', 'build', 'node_modules', '.idea', '.vscode', 'venv', '__pycache__'
        )
        
        shutil.copytree(self.project_root, self.sandbox_root, ignore=ignore)

    def map_path(self, original_path: Path) -> Path:
        """Converts /app/src/Main.java -> /app/.modernizer_sandbox/src/Main.java"""
        rel_path = original_path.resolve().relative_to(self.project_root)
        return self.sandbox_root / rel_path

    def cleanup(self):
        if self.sandbox_root.exists():
            shutil.rmtree(self.sandbox_root)