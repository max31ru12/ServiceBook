from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import BaseAsyncSQLAlchemyRepository
from app.domains.users.models import User


class UserRepository(BaseAsyncSQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self) -> Sequence[User]:
        return (await self.session.execute(select(User))).scalars().all()

    async def get_by_id(self, user_id: int) -> User | None:
        return (
            await self.session.execute(select(User).filter_by(id=user_id))
        ).scalar_one_or_none()

    async def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.session.add(user)
        await self.session.commit()
        return user

    async def update(self, user_id: int) -> None:
        await self.session.execute(update(User).where(User.id == user_id))

    async def remove(self, user_id: int) -> None:
        await self.session.execute(delete(User).where(User.id == user_id))
