import typer
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from typing import Optional

# Local Imports
from .config import settings
from .engine.refactor import RefactorEngine
from .engine.compiler import Compiler
from .engine.sandbox import SandboxManager
from .strategies.reactive import WebFluxStrategy
# Graceful import for AI
try:
    from .agent.llm import LLMClient
except ImportError:
    LLMClient = None

app = typer.Typer(help="Neuro-Symbolic Migration Agent", add_completion=False)
console = Console()

@app.command()
def migrate(
    path: Path = typer.Argument(..., exists=True, help="Path to file or repo"),
    target: str = typer.Option("webflux", help="Target architecture"),
    dry_run: bool = typer.Option(False, help="Skip saving to disk"),
    auto_approve: bool = typer.Option(False, help="Batch mode (no prompts)")
):
    """
    🚀 Interactive Migration Pipeline: Sandbox -> Refactor -> AI Fix -> Verify
    """
    strategy = WebFluxStrategy()
    
    # 1. Project Detection
    project_root = path.parent
    if "src" in str(path):
        curr = path
        while curr.parent != curr:
            if (curr / "pom.xml").exists() or (curr / "build.gradle").exists():
                project_root = curr
                break
            curr = curr.parent

    # 2. Sandbox Setup
    sandbox = SandboxManager(project_root)
    with console.status(f"[bold green]📦 Creating sandbox for {project_root.name}..."):
        sandbox.create()

    # 3. File Discovery
    files = [path] if path.is_file() else list(path.rglob("*.java"))
    console.print(Panel(f"Found {len(files)} files to process", title="Audit", border_style="blue"))

    # Initialize AI
    llm = LLMClient() if (LLMClient and settings.openai_api_key) else None

    # 4. Processing Loop
    for original_file in track(files, description="Migrating..."):
        sandbox_file = sandbox.map_path(original_file)
        engine = RefactorEngine(sandbox_file)

        # Optimization: Skip files that don't need help
        if not strategy.needs_migration(engine.content):
            continue

        # Phase 1: Deterministic Changes
        engine.apply_recipes(strategy.get_recipes())

        # Phase 2: AI Refactoring
        target_sig = "public void start(Promise<Void> startFuture)" # Example hotspot
        legacy_code = engine.extract_method(target_sig)
        
        compilation_passed = False
        
        if legacy_code and llm:
            console.print(f"\n[cyan]🧠 AI Refactoring: {original_file.name}[/cyan]")
            new_code = llm.refactor_code(legacy_code, strategy.prompt(legacy_code))
            
            # Self-Healing Loop
            for attempt in range(3):
                if not new_code: break
                
                engine.replace_method(target_sig, new_code)
                engine.save()
                
                # Check Build
                compiler = Compiler(sandbox.sandbox_root)
                success, error = compiler.check_build()
                
                if success:
                    compilation_passed = True
                    console.print("  [green]✅ Build Passed[/green]")
                    break
                else:
                    console.print(f"  [red]❌ Attempt {attempt+1} failed. Re-prompting AI...[/red]")
                    new_code = llm.refactor_code(new_code, strategy.fix_prompt(new_code, error))

        # Phase 3: Interactive Approval
        if engine.has_changes(original_file):
            engine.show_diff(original_file)
            
            if not dry_run:
                if auto_approve or typer.confirm(f"Apply changes to {original_file.name}?"):
                    shutil.copy2(sandbox_file, original_file)
                    console.print(f"[green]✔ Saved {original_file.name}[/green]")
                else:
                    console.print("[dim]Skipped[/dim]")

    if not dry_run:
        sandbox.cleanup()
    console.print("[bold green]✨ Migration Complete![/bold green]")

if __name__ == "__main__":
    app()