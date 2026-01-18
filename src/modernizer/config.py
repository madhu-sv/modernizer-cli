import os
from typing import Optional
from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Modernizer CLI"
    debug_mode: bool = False
    
    # --- LLM Configuration ---
    # Updated default to Claude Sonnet 4.5 (Sept 2025 Release)
    llm_provider: str = Field(default="anthropic", description="Provider: 'anthropic' or 'openai'")
    llm_model: str = Field(
        default="claude-sonnet-4-5-20250929", 
        description="The specific model ID (e.g., claude-sonnet-4-5-20250929)"
    )
    
    # Temperature 0 is still best for deterministic refactoring
    llm_temperature: float = Field(default=0.0, ge=0.0, le=1.0)

    # --- API Keys (Conditional Validation) ---
    # We make them optional here so the app doesn't crash if you have one but not the other.
    # Logic in llm.py checks for the specific key needed.
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        # 'ignore' allows extra keys in .env without crashing
        extra="ignore"
    )

# Robust Initialization
try:
    settings = Settings()
except ValidationError as e:
    print("❌ Configuration Error: Missing required environment variables.")
    # Print clean error messages for missing fields
    for error in e.errors():
        field = error['loc'][0]
        print(f"   - {field}: Field required")
    exit(1)