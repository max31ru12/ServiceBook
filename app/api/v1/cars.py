from fastapi import APIRouter

from app.core.requests import OrderingDep, PaginationParamsDep
from app.core.responses import InvalidRequestParamsResponses, PaginatedResponse
from app.domains.cars.dependencies import BrandServiceDep, CarServiceDep
from app.domains.cars.schemas import Brand, CarData

cars_router = APIRouter(prefix="/cars", tags=["cars"])


class CarListResponses(InvalidRequestParamsResponses):
    pass


@cars_router.get(
    "/",
    status_code=200,
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
    except AttributeError:
        raise CarListResponses.INVALID_SORTER_FIELD

    car_list = [CarData.model_validate(car, from_attributes=True) for car in cars]
    cars_count = await service.get_cars_count()

    return PaginatedResponse(count=cars_count, data=car_list)


class BrandListResponses(InvalidRequestParamsResponses):
    pass


@cars_router.get(
    "/brands",
    status_code=200,
    response_model=PaginatedResponse[Brand],
    responses=BrandListResponses.get_responses(),
)
async def get_all_brands(
    pagination: PaginationParamsDep,
    service: BrandServiceDep,
    ordering: OrderingDep = None,
) -> PaginatedResponse[Brand]:
    limit = pagination.page_size
    offset = limit * (pagination.page - 1)

    try:
        brands = await service.get_all_brands(limit, offset, sort_by=ordering)
    except AttributeError:
        raise BrandListResponses.INVALID_SORTER_FIELD

    brand_list = [Brand.model_validate(row, from_attributes=True) for row in brands]
    brands_count = await service.get_brands_count()

    return PaginatedResponse(count=brands_count, data=brand_list)
