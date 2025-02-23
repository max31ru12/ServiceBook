from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, TypeVar

from sqlalchemy import delete, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.utils.exceptions import InvalidSorterError


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

    async def list(self, limit: int = None, offset: int = None, sort_by: str = None):
        stmt = select(self.model)

        if limit is not None and offset is not None:
            stmt = stmt.limit(limit).offset(offset)

        if sort_by is not None:
            for param in sort_by.split(","):
                if not hasattr(self.model, param.strip("-")):
                    raise InvalidSorterError(f"Model <{self.model.__name__}> don't have attribute <{param}>")
            stmt = stmt.order_by(text(sort_by))

        return (await self.session.execute(stmt)).scalars().all()

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        return instance

    async def update(self, row_id: int, update_data: dict[str | Any]):
        return await self.session.execute(
            update(self.model).where(self.model.id == row_id).values(**update_data).returning(self.model.id)
        )

    async def remove(self, row_id: int):
        return await self.session.execute(delete(self.model).where(self.model.id == row_id).returning(self.model.id))

    async def get_by_id(self, model_id: int) -> ModelType:
        return (await self.session.execute(select(self.model).filter_by(id=model_id))).scalar_one_or_none()

    async def get_by_kwargs(self, **kwargs) -> Sequence[ModelType]:
        return (await self.session.execute(select(self.model).filter_by(**kwargs))).scalars().all()

    async def get_first_by_kwargs(self, **kwargs) -> ModelType:
        return (await self.session.execute(select(self.model).filter_by(**kwargs))).scalars().first()

    async def get_count(self) -> int:
        return (await self.session.execute(select(func.count()).select_from(self.model))).scalar()

    async def join(self, model_field) -> ModelType:
        stmt = select(self.model).options(joinedload(model_field))
        return (await self.session.execute(stmt)).scalars().all()
