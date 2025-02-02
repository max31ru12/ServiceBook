from fastapi import APIRouter

from app.domains.users.dependencies import CurrentUserDep
from app.domains.users.schemas import UserData

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=UserData)
async def get_current_user(user: CurrentUserDep) -> UserData:
    return UserData.from_orm(user)
