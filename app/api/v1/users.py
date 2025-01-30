from fastapi import APIRouter

from app.domains.users.dependencies import CurrentUserDep, UserServiceDep
from app.domains.users.schemas import UserData

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me")
async def get_current_user(user: CurrentUserDep) -> UserData:
    return UserData.from_orm(user)


@users_router.get("/first")
async def get_first_user(service: UserServiceDep):
    user = await service.get_user_by_id(1)
    return user
