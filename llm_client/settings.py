from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration for the LLM client."""

    base_url: str = "http://localhost:11434/v1"
    api_key: str = "ollama"
    model: str = "llama3.2"
    timeout: float = 30.0
    max_retries: int = 3

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LLM_",
        extra="ignore",
    )


settings = Settings()
