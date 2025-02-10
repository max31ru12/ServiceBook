from fastapi import APIRouter
from fastapi.params import Path, Query

from app.core.requests import PaginationParamsDep
from app.core.responses import PaginatedResponse
from app.domains.cars.dependencies import CarServiceDep
from app.domains.cars.schemas import CarData

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
    response_model=PaginatedResponse[CarData],
)
async def get_all_cars(
    pagination: PaginationParamsDep, service: CarServiceDep
) -> PaginatedResponse[CarData]:
    limit = pagination.page_size
    offset = limit * (pagination.page - 1)
    cars = await service.get_all_cars(limit, offset)

    car_list = [CarData.model_validate(car, from_attributes=True) for car in cars]
    cars_count = await service.get_cars_count()

    return PaginatedResponse(count=cars_count, data=car_list)
