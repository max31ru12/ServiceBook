from fastapi import APIRouter
from fastapi.params import Path, Query

from app.core.requests import OrderingDep, PaginationParamsDep
from app.core.responses import PaginatedResponse, Responses
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


class CarListResponses(Responses):

    INVALID_FILTER_FIELD = 400, "Invalid filter field"
    INVALID_SORTER_FIELD = 400, "Invalid sorter field"


@cars_router.get(
    "/",
    response_model=PaginatedResponse[CarData],
    responses=CarListResponses.get_responses(),
)
async def get_all_cars(
    pagination: PaginationParamsDep,
    service: CarServiceDep,
    ordering: OrderingDep = None,
) -> PaginatedResponse[CarData]:
    limit = pagination.page_size
    offset = limit * (pagination.page - 1)

    try:
        cars = await service.get_all_cars(limit, offset, sort_by=ordering)

        car_list = [CarData.model_validate(car, from_attributes=True) for car in cars]
        cars_count = await service.get_cars_count()
    except AttributeError:
        raise CarListResponses.INVALID_SORTER_FIELD

    return PaginatedResponse(count=cars_count, data=car_list)
