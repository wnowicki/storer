from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(str, Enum):
    """Application environment."""

    DEV = "development"
    PROD = "production"
    TEST = "testing"


class AppSettings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    release_version: str

    env: Env = Env.DEV

    secret_key: str

    jwt_algorithm: str = "HS256"
    jwt_access_token_expire: int = 1800  # 30 minutes

    log_level: str = "INFO"

    log_local: bool = True
    log_file_max_bytes: int = 1000000
    log_file_backup_count: int = 5

    database_url: str
