from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.cars.models import Brand, Car
from app.domains.cars.repositories import BrandRepository, CarRepository


class CarService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = CarRepository(session)

    async def get_car_by_id(self, user_id: int) -> Car:
        return await self.repository.get_by_id(user_id)

    async def get_car_by_kwargs(self, **kwargs) -> Car:
        return await self.repository.get_first_by_kwargs(**kwargs)

    async def get_all_cars(self, limit: int = None, offset: int = None, sort_by: str = None) -> Sequence[Car]:
        return await self.repository.list(limit, offset, sort_by)

    async def get_cars_count(self) -> int:
        return await self.repository.get_count()

    async def get_cars_joined_brand(self) -> Car:
        return await self.repository.join(Car.brand)


class BrandService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = BrandRepository(session)

    async def get_all_brands(self, limit: int = None, offset: int = None, sort_by: str = None) -> Sequence[Brand]:
        return await self.repository.list(limit, offset, sort_by)

    async def get_brands_count(self) -> int:
        return await self.repository.get_count()
