from fastapi import APIRouter

cars_router = APIRouter(prefix="/cars", tags=["cars"])


@cars_router.get("/")
async def get_all_cars() -> str:
    return "All cars"
