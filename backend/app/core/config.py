from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpenUASLog"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./data/openuaslog.db"
    secret_key: str = "change-this-secret-in-production"
    token_expire_minutes: int = 480
    cors_origins: str = "http://localhost:5173,http://localhost:8080"
    initial_admin_username: str = "admin"
    initial_admin_email: str = "admin@example.com"
    initial_admin_password: str = "admin"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="OPENUASLOG_",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def ensure_sqlite_directory(self) -> None:
        prefix = "sqlite:///"
        if not self.database_url.startswith(prefix):
            return
        database_path = self.database_url.removeprefix(prefix)
        if database_path == ":memory:":
            return
        Path(database_path).expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
