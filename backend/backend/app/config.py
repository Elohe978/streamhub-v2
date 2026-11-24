from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "StreamHub API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    demo_hls_url: str = ""
    database_url: str = "postgresql+asyncpg://streamhub:change-this-local-password@localhost:5432/streamhub"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
