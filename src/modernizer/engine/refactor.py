import re
import difflib
from pathlib import Path
from typing import Optional, List, Dict
from rich.console import Console
from rich.syntax import Syntax

console = Console()

class RefactorEngine:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.original_content = file_path.read_text(encoding="utf-8")
        self.content = self.original_content

    def extract_method(self, signature_hint: str) -> Optional[str]:
        """Extracts a method body using brace counting."""
        start = self.content.find(signature_hint)
        if start == -1: return None
        
        brace_start = self.content.find("{", start)
        if brace_start == -1: return None

        count = 0
        for i, char in enumerate(self.content[brace_start:], start=brace_start):
            if char == '{': count += 1
            elif char == '}': count -= 1
            
            if count == 0:
                return self.content[start : i+1]
        return None

    def replace_method(self, signature_hint: str, new_code: str):
        old_code = self.extract_method(signature_hint)
        if old_code and old_code in self.content:
            self.content = self.content.replace(old_code, new_code)

    def apply_recipes(self, recipes: Dict[str, str]):
        """Applies simple regex replacements (imports, annotations)."""
        for old, new in recipes.items():
            if old in self.content:
                self.content = self.content.replace(old, new)

    def has_changes(self, comparison_file: Path) -> bool:
        return self.content != comparison_file.read_text(encoding="utf-8")

    def show_diff(self, comparison_file: Path):
        original = comparison_file.read_text(encoding="utf-8").splitlines()
        modified = self.content.splitlines()
        
        diff = difflib.unified_diff(
            original, modified,
            fromfile=f"Original: {comparison_file.name}",
            tofile="Migrated (Sandbox)",
            lineterm=""
        )
        syntax = Syntax("\n".join(diff), "diff", theme="monokai", line_numbers=True)
        console.print(syntax)

    def save(self):
        self.file_path.write_text(self.content, encoding="utf-8")