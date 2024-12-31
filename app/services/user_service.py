from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from app.models.user import User
from app.setup_db import session_getter


async def get_user_db(session: AsyncSession = Depends(session_getter)):
    yield SQLAlchemyUserDatabase(session, User)