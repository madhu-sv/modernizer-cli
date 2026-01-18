import subprocess
import platform
from pathlib import Path
from typing import Tuple, Optional
from rich.console import Console

console = Console()

class Compiler:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.build_system = self._detect_build_system()

    def _detect_build_system(self) -> str:
        if (self.project_root / "build.gradle").exists() or \
           (self.project_root / "build.gradle.kts").exists():
            return "gradle"
        return "maven"

    def check_build(self) -> Tuple[bool, Optional[str]]:
        """Returns (Success, ErrorLog)."""
        if self.build_system == "gradle":
            return self._run_gradle()
        return self._run_maven()

    def _run_maven(self):
        console.print("[dim]🔨 running 'mvn clean compile'...[/dim]")
        try:
            result = subprocess.run(
                ["mvn", "clean", "compile", "-DskipTests"], 
                cwd=self.project_root,
                capture_output=True, text=True
            )
            return self._parse_output(result, "[ERROR]")
        except FileNotFoundError:
            return False, "Maven executable not found."

    def _run_gradle(self):
        wrapper = "./gradlew" if platform.system() != "Windows" else "gradlew.bat"
        cmd = str(self.project_root / wrapper) if (self.project_root / wrapper).exists() else "gradle"
        
        console.print(f"[dim]🔨 running '{Path(cmd).name} clean compileJava'...[/dim]")
        try:
            result = subprocess.run(
                [cmd, "clean", "compileJava", "-x", "test", "--no-daemon", "--console=plain"], 
                cwd=self.project_root,
                capture_output=True, text=True
            )
            return self._parse_output(result, "error:")
        except Exception as e:
            return False, str(e)

    def _parse_output(self, result, error_keyword):
        if result.returncode == 0:
            return True, None
        
        # Filter for relevant lines to save context window
        log = result.stdout + result.stderr
        errors = [line for line in log.splitlines() if error_keyword in line or "FAILED" in line]
        summary = "\n".join(errors[:15]) if errors else "\n".join(log.splitlines()[-20:])
        return False, summary