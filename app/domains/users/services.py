from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_password_hash
from app.domains.users.models import User
from app.domains.users.repositories import UserRepository
from app.domains.users.schemas import CreateUser


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_kwargs(self, **kwargs) -> User:
        return await self.repository.get_first_by_kwargs(**kwargs)

    async def get_all_users(self) -> Sequence[User]:
        return await self.repository.list()

    async def create_user(self, user_data: CreateUser) -> User:
        user_data.password = get_password_hash(user_data.password)
        return await self.repository.create(**user_data.dict())
