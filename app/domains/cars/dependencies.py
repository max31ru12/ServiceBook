from typing import Annotated

from fastapi import Depends

from app.domains.cars.services import CarService

CarServiceDep = Annotated[CarService, Depends(CarService)]
