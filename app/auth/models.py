from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from app.setup_db import Base, session_getter


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @classmethod
    async def get_user_db(cls, session: AsyncSession = Depends(session_getter)):
        yield SQLAlchemyUserDatabase(session, User)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    @declared_attr
    def user_id(self):
        return Column(
            Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
        )

    @classmethod
    async def get_access_token_db(cls, session: AsyncSession = Depends(session_getter)):
        yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
