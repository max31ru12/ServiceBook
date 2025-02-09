from typing import Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.setup_db import session_getter
from app.domains.cars.models import Car
from app.domains.cars.repositories import CarRepository


class CarService:
    def __init__(self, session: AsyncSession = Depends(session_getter)):
        self.session = session
        self.repository = CarRepository(session)

    async def get_car_by_id(self, user_id: int) -> Car:
        return await self.repository.get_by_id(user_id)

    async def get_car_by_kwargs(self, **kwargs) -> Car:
        return await self.repository.get_first_by_kwargs(**kwargs)

    async def get_all_cars(
        self, limit: int = None, offset: int = None
    ) -> Sequence[Car]:
        return await self.repository.list(limit, offset)

    async def get_cars_joined_brand(
        self, limit: int = None, offset: int = None
    ) -> Sequence[Car]:
        return await self.repository.get_cars_joined_brand()
