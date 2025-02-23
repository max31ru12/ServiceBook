from typing import Any, Sequence

from app.core.utils.auth import get_password_hash
from app.domains.users.models import User
from app.domains.users.schemas import CreateUser
from app.domains.users.uow import UsersUnitOfWork


class UserService:
    def __init__(self):
        self.uow = UsersUnitOfWork()

    async def get_user_by_id(self, user_id: int) -> User:
        async with self.uow:
            user = await self.uow.user_repository.get_by_id(user_id)
        return user

    async def get_user_by_kwargs(self, **kwargs) -> User:
        async with self.uow:
            return await self.uow.user_repository.get_first_by_kwargs(**kwargs)

    async def get_all_users(self, limit: int = None, offset: int = None, sort_by: str = None) -> Sequence[User]:
        async with self.uow:
            return await self.uow.user_repository.list(limit, offset, sort_by)

    async def create_user(self, user_data: CreateUser) -> User:
        async with self.uow:
            user_data.password = get_password_hash(user_data.password)
            user = await self.uow.user_repository.create(**user_data.dict())
            return user

    async def update_user(self, user_id: int, update_user_data: dict[str | Any]):
        async with self.uow:
            return await self.uow.user_repository.update(user_id, update_user_data)

    async def delete_user(self, user_id: int) -> None:
        async with self.uow:
            return await self.uow.user_repository.remove(user_id)

    async def get_users_count(self) -> int:
        async with self.uow:
            return await self.uow.user_repository.get_count()
