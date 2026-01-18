from typing import Optional
from rich.console import Console
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from ..config import settings

console = Console()

class LLMClient:
    def __init__(self):
        self.provider = settings.llm_provider.lower()
        self.model_name = settings.llm_model
        
        console.print(f"[dim]🧠 Initializing Brain: [bold cyan]{self.provider}[/bold cyan] ({self.model_name})[/dim]")

        if self.provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("❌ ANTHROPIC_API_KEY is missing from .env")
            
            self.llm = ChatAnthropic(
                model=self.model_name,
                temperature=settings.llm_temperature,
                api_key=settings.anthropic_api_key,
                # UPDATE: Sonnet 4.5 supports 64k output tokens. 
                # This ensures it can rewrite 2000+ line files in one go.
                max_tokens=64000,
                max_retries=3
            )
            
        elif self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError("❌ OPENAI_API_KEY is missing from .env")
            
            self.llm = ChatOpenAI(
                model=settings.llm_model, 
                temperature=settings.llm_temperature,
                api_key=settings.openai_api_key
            )

    def refactor_code(self, code_snippet: str, system_prompt: str) -> Optional[str]:
        """
        Sends code to the LLM. Returns None on failure.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "{code}")
        ])

        chain = prompt | self.llm

        try:
            console.print("[dim]🧠 Thinking...[/dim]")
            response = chain.invoke({"code": code_snippet})
            return self._clean_markdown(response.content)
        except Exception as e:
            console.print(f"[red]❌ LLM Call Failed: {e}[/red]")
            return None

    def _clean_markdown(self, text: str) -> str:
        """Strips markdown code blocks from the response."""
        if not text: return ""
        text = text.strip()
        if text.startswith("```"):
            first_newline = text.find("\n")
            if first_newline != -1:
                text = text[first_newline+1:]
            if text.endswith("```"):
                text = text[:-3]
        return text.strip()