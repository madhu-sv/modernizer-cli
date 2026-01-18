# 🚀 Modernizer CLI
Modernizer is an intelligent, Neuro-Symbolic Agent designed to automate the migration of legacy Java applications (e.g., Vert.x, Java 8) to modern stacks (Spring Boot 3, Java 21, WebFlux).

Unlike standard "chat-with-code" tools, Modernizer uses a "Plan-and-Execute" architecture. It combines the deterministic safety of traditional refactoring engines with the reasoning capabilities of LLMs to fix logic, compile code, and heal build errors automatically.

# 🧠 Architecture & Workflow
Sandbox Isolation: The agent copies your repo to a hidden .modernizer_sandbox/ folder. No changes touch your real code until verification passes.

Deterministic Refactoring: It uses Regex/AST to instantly fix imports, annotations, and dependencies (0% hallucination).

Neural Refactoring: It extracts complex logic (e.g., Verticle.start()) and asks the LLM to rewrite it using modern patterns (e.g., Reactor Mono/Flux).

Self-Healing Loop: It runs mvn compile or ./gradlew compileJava. If the build fails, it feeds the error back to the LLM to fix the code.

Human Verification: It presents a color-coded Diff. If you approve, the file is promoted to the main repository.

# ✨ Key Features
🛡️ Safety First: Non-destructive sandboxing ensures your git tree remains clean during experimentation.

🔌 Build System Agnostic: Auto-detects Maven (pom.xml) and Gradle (build.gradle), using local wrappers (./gradlew) when available.

💊 Self-Healing: The agent doesn't just write code; it fixes its own compilation errors before asking for your review.

⚡ Batch Mode: Run with --auto-approve for CI/CD pipelines or large-scale migrations.

🐳 Single Binary: Compiles to a standalone executable for easy distribution.

# 🛠️ Development Setup
Follow these steps to set up a robust development environment.

1. Prerequisites
Python 3.9+

Java JDK 17+ (Required to run the compilation checks)

Maven or Gradle installed (or available via wrappers in your target projects)

2. Clone the Repository
   
  git clone https://github.com/your-username/modernizer-cli.git
  cd modernizer-cli
  
3. Create a Virtual Environment
We recommend using venv to keep dependencies isolated.

Mac/Linux:

    python3 -m venv venv
    source venv/bin/activate
Windows (PowerShell):

PowerShell

    python -m venv venv
    .\venv\Scripts\Activate.ps1

4. Install in Editable Mode
We use pip install -e so changes in the src/ folder are immediately reflected in the CLI without reinstalling. We also install [dev] dependencies (testing tools).

Bash

    pip install -e .[dev]
5. Configure Environment Variables
The agent needs an API Key to perform neural refactoring.

Copy the example file:

Bash

    cp .env.example .env
Edit .env and add your OpenAI/Anthropic  Key:

Ini, TOML

    OPENAI_API_KEY=sk-proj-12345...
    ANTHROPIC_API_KEY=sk-proj-124...
    LLM_MODEL=gpt-4o  # Optional, defaults to gpt-4o
    
6. Verify Installation
Run the help command to ensure the CLI is linked correctly.

Bash

    modernizer --help
Output should display the "Neuro-Symbolic Migration Agent" banner.

# 🚀 Usage
Audit a Repository
Scan a folder to see which files require migration.

Bash

    modernizer audit /path/to/legacy-repo --target webflux
    Run a Migration
    Migrate a single file or an entire folder.

    Interactive Mode (Recommended for first run):

Bash

    modernizer migrate /path/to/legacy-repo/src/main/java/com/app/OldVerticle.java
    Batch Mode (For confident runs):

Bash

    modernizer migrate /path/to/legacy-repo --auto-approve
    Dry Run (Safe mode):

Bash

    modernizer migrate /path/to/legacy-repo --dry-run
# 🧪 Testing
We use Pytest for unit and integration testing.

Bash

    # Run all tests
    pytest tests/

    # Run with verbose output
    pytest -v tests/

# CI/CD Integration
The project includes GitHub Actions workflows in .github/workflows/:

    ci.yml: Runs pytest on every Push/PR.

    release.yml: Builds a binary executable when a new Tag (e.g., v1.0.0) is pushed.

# 📦 Building a Binary
To distribute the tool to developers who don't have Python installed, build a standalone binary:

Bash

    # Requires pyinstaller (installed via .[dev])
    pyinstaller --onefile --name modernizer src/modernizer/main.py
The executable will appear in the dist/ folder.

# 📄 License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
