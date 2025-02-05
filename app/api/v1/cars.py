from fastapi import APIRouter
from fastapi.params import Path, Query

cars_router = APIRouter(prefix="/cars", tags=["cars"])


@cars_router.get("/{car_id}")
async def get_all_cars(
    page: int = Query(..., title="Page number", ge=1),
    page_size: int = Query(..., title="Page size", ge=1),
    car_id: int = Path(..., title="Car id", ge=1),
) -> str:
    return f"All cars"
