from typing import Annotated

from fastapi import Depends

from app.core.setup_db import AsyncSessionDep
from app.domains.cars.services import BrandService, CarService


def get_car_service(session: AsyncSessionDep) -> CarService:
    return CarService()


def get_brand_service(session: AsyncSessionDep) -> BrandService:
    return BrandService()


CarServiceDep = Annotated[CarService, Depends(get_car_service)]
BrandServiceDep = Annotated[BrandService, Depends(get_brand_service)]
