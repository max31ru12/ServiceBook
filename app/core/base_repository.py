from abc import ABC, abstractmethod
from typing import Generic, TypeVar


class BaseRepository(ABC):
    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model_id: int):
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


class BaseAsyncSQLAlchemyRepository(BaseRepository, ABC, Generic[ModelType]):
    @abstractmethod
    async def list(self) -> list[ModelType]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, model_id: int) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def create(self) -> ModelType:
        raise NotImplementedError

    @abstractmethod
    async def update(self, model_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, model_id: int) -> None:
        raise NotImplementedError
