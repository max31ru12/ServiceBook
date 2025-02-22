from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

DEV_MODE: bool = getenv("DEV_MODE", "true") == "true"

BASE_DIR = Path(__file__).parent.parent

# Alembic constraint naming convention
CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Settings(BaseSettings):
    ACCESS_TOKEN_LIFETIME_MINUTES: int = 15
    REFRESH_TOKEN_LIFETIME_DAYS: int = 30
    REFRESH_TOKEN_LIFETIME_DAYS_NOT_REMEMBER: int = 1

    # DB settings
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_PASSWORD: str = "test"
    DB_USER: str = "test"
    DB_NAME: str = "test"

    APP_HOST: str = "127.0.0.1"  # Для локального запуска

    RESET_PASSWORD_TOKEN_SECRET: str = "reset_password_token"
    VERIFICATION_TOKEN_SECRET: str = "verification_token"

    SECRET_KEY: str = "gV64m9aIzFG4qpgVphvQbPQrtAO0nM-7YwwOvu0XPt5KJOjAy4AfgLkqJXYEt"
    ALGORITHM: str = "HS256"

    class ConfigDict:
        env = BASE_DIR / ".env"


settings = Settings()

DB_URL: str = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
