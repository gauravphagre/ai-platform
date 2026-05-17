from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ai-platform"
    DEBUG: bool = True
    OLLAMA_BASE_URL: str = "http://ollama:11434"
    DEFAULT_MODEL: str = "qwen2.5-coder:7b"

    class Config:
        env_file = ".env"


settings = Settings()