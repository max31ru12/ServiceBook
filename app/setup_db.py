from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import CONVENTION, DEV_MODE, settings

async_engine: AsyncEngine = create_async_engine(
    url=settings.DB_URL,
    echo=DEV_MODE,
    pool_size=10,
    max_overflow=20,
)
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def session_getter() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=CONVENTION)

    def __repr__(self):
        instance_id = f" id={self.id}" if hasattr(self, "id") else ""
        return f"{self.__class__.__name__}{instance_id}"
