from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def get(self, model_id: int):
        raise NotImplementedError

    @abstractmethod
    def create(self):
        raise NotImplementedError

    @abstractmethod
    def update(self, model_id: int):
        raise NotImplementedError

    @abstractmethod
    def remove(self, model_id: int):
        raise NotImplementedError


ModelType = TypeVar("ModelType")


class BaseAsyncSQLAlchemyRepository(ABC, Generic[ModelType]):

    model: ModelType = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def list(self, limit: int = None, offset: int = None):
        if limit is not None and offset is not None:
            return (
                (
                    await self.session.execute(
                        select(self.model).limit(limit).offset(offset)
                    )
                )
                .scalars()
                .all()
            )
        return (await self.session.execute(select(self.model))).scalars().all()

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def remove(self, model_id: int):
        return await self.session.execute(
            delete(self.model).where(self.model.id == model_id)
        )

    async def get_by_id(self, model_id: int) -> ModelType:
        return (
            await self.session.execute(select(self.model).filter_by(id=model_id))
        ).scalar_one_or_none()

    async def get_by_kwargs(self, **kwargs) -> Sequence[ModelType]:
        return (
            (await self.session.execute(select(self.model).filter_by(**kwargs)))
            .scalars()
            .all()
        )

    async def get_first_by_kwargs(self, **kwargs) -> ModelType:
        return (
            (await self.session.execute(select(self.model).filter_by(**kwargs)))
            .scalars()
            .first()
        )

    async def get_count(self):
        return (
            await self.session.execute(select(func.count()).select_from(self.model))
        ).scalar()
