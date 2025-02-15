from typing import Annotated

from fastapi import Depends

from app.core.setup_db import AsyncSessionDep
from app.domains.cars.services import CarService


def get_car_service(session: AsyncSessionDep) -> CarService:
    return CarService(session)


CarServiceDep = Annotated[CarService, Depends(get_car_service)]
