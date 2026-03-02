from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GEMINI_API_KEY: str
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    PROMPTS_DIR: Path = BASE_DIR / "prompts"
    HEADER_AUTH_KEY: Optional[str] = None


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()