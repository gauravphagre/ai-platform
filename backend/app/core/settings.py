from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ai-platform"
    DEBUG: bool = True

    DATABASE_URL: str = (
        "postgresql+asyncpg://ai_user:ai_password@postgres:5432/ai_platform"
    )

    OLLAMA_BASE_URL: str = "http://ollama:11434"
    DEFAULT_MODEL: str = "qwen2.5-coder:7b"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )



settings = Settings()