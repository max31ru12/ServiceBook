from fastapi import APIRouter
from fastapi.params import Path, Query

from app.domains.cars.dependencies import CarServiceDep
from app.domains.cars.schemas import Car

cars_router = APIRouter(prefix="/cars", tags=["cars"])


@cars_router.get("/{car_id}")
async def get_car(
    page: int = Query(..., title="Page number", ge=1),
    page_size: int = Query(..., title="Page size", ge=1),
    car_id: int = Path(..., title="Car id", ge=1),
) -> str:
    return f"All cars"


@cars_router.get(
    "/",
    response_model=list[Car],
)
async def get_all_cars(service: CarServiceDep) -> list[Car]:
    cars = await service.get_all_cars()
    return [Car.from_orm(car) for car in cars]
