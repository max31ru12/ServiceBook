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
    LIFETIME: int = 60 * 60 * 24

    # DB settings
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_PASSWORD: str = "test"
    DB_USER: str = "test"
    DB_NAME: str = "test"

    DB_URL: str = (
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    PUBLIC_KEY: str = "public"
    PRIVATE_KEY: str = "private"

    class ConfigDict:
        env = ".env"


settings = Settings()
