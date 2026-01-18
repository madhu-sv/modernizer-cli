from typing import Dict, List

class WebFluxStrategy:
    """Strategy for migrating Vert.x to Spring WebFlux."""

    def needs_migration(self, content: str) -> bool:
        return "Verticle" in content or "Future" in content or "Promise" in content

    def get_recipes(self) -> Dict[str, str]:
        """Deterministic replacements (Imports/Annotations)."""
        return {
            "io.vertx.core.AbstractVerticle": "org.springframework.stereotype.Service",
            "io.vertx.core.Promise": "reactor.core.publisher.Mono",
            "extends AbstractVerticle": "", # Remove inheritance
            "import io.vertx.core.json.JsonObject;": "import com.fasterxml.jackson.databind.JsonNode;"
        }

    def prompt(self, code: str) -> str:
        return """
You are a Senior Java Architect. Refactor the following Legacy Vert.x code to Spring Boot 3 (WebFlux).

RULES:
1. Replace 'start(Promise)' with a '@PostConstruct public void init()' method.
2. Replace Vert.x 'Future' with Project Reactor 'Mono' or 'Flux'.
3. Do NOT use Thread.sleep(). Use Mono.delay() if strictly necessary.
4. Return ONLY the Java method body. No markdown.
"""

    def fix_prompt(self, code: str, error: str) -> str:
        return f"""
The refactored code failed to compile.
ERROR: {error}

CODE:
{code}

TASK: Fix the code to satisfy the compiler. Return ONLY the fixed Java code.
"""