from fastapi import APIRouter

from app.domains.users.dependencies import CurrentUser
from app.domains.users.schemas import UserData

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me")
async def get_current_user(user: CurrentUser) -> UserData:
    return UserData.from_orm(user)
