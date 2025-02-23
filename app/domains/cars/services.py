from typing import Sequence

from app.domains.cars.models import Brand, Car
from app.domains.cars.uow import CarsUnitOfWork


class CarService:
    def __init__(self):
        self.uow = CarsUnitOfWork()

    async def get_car_by_id(self, user_id: int) -> Car:
        async with self.uow:
            return await self.uow.car_repository.get_by_id(user_id)

    async def get_car_by_kwargs(self, **kwargs) -> Car:
        async with self.uow:
            return await self.uow.car_repository.get_first_by_kwargs(**kwargs)

    async def get_all_cars(self, limit: int = None, offset: int = None, sort_by: str = None) -> Sequence[Car]:
        async with self.uow:
            return await self.uow.car_repository.list(limit, offset, sort_by)

    async def get_cars_count(self) -> int:
        async with self.uow:
            return await self.uow.car_repository.get_count()

    async def get_cars_joined_brand(self) -> Car:
        async with self.uow:
            return await self.uow.car_repository.join(Car.brand)


class BrandService:
    def __init__(self):
        self.uow = CarsUnitOfWork()

    async def get_all_brands(self, limit: int = None, offset: int = None, sort_by: str = None) -> Sequence[Brand]:
        async with self.uow:
            return await self.uow.brand_repository.list(limit, offset, sort_by)

    async def get_brands_count(self) -> int:
        async with self.uow:
            return await self.uow.brand_repository.get_count()
