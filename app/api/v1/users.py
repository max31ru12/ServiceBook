from fastapi import APIRouter, Depends
from sqlalchemy import select

from app.core.setup_db import session_factory, session_getter
from app.domains.users.models import User
from app.domains.users.schemas import LoginForm

users_router = APIRouter(prefix="/users")


@users_router.post("/login")
async def login(data: LoginForm, session=Depends(session_getter)):
    async with session_factory() as session:
        stmt = select(User).where(User.username == data.username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

    return {"username": user.username}
