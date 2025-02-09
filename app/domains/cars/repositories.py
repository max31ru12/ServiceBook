from typing import Sequence

from sqlalchemy import select

from app.core.base_repository import BaseAsyncSQLAlchemyRepository
from app.domains.cars.models import Brand, Car


class BrandRepository(BaseAsyncSQLAlchemyRepository):
    model = Brand


class CarRepository(BaseAsyncSQLAlchemyRepository):
    model = Car

    async def get_cars_joined_brand(
        self, limit: int = None, offset: int = None
    ) -> Sequence[Car]:
        async with self.session:
            stmt = select(Car).join_from(Car, Brand).limit(limit).offset(offset)
            cars = await self.session.execute(stmt)
        return cars.scalars().all()
