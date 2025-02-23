from fastapi import APIRouter

from app.core.requests import OrderingDep, PaginationParamsDep
from app.core.responses import InvalidRequestParamsResponses, PaginatedResponse, Responses
from app.domains.users.dependencies import CurrentUserDep, UserServiceDep
from app.domains.users.schemas import UpdateUserData, UserData

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=UserData)
async def get_current_user(user: CurrentUserDep) -> UserData:
    return UserData.from_orm(user)


class UserListResponses(InvalidRequestParamsResponses):
    pass


@users_router.get(
    "/",
    responses=UserListResponses.get_responses(),
)
async def get_all_users(
    pagination: PaginationParamsDep,
    user_service: UserServiceDep,
    ordering: OrderingDep = None,
) -> PaginatedResponse[UserData]:
    limit = pagination.page_size
    offset = limit * (pagination.page - 1)

    try:
        users = await user_service.get_all_users(limit, offset, sort_by=ordering)
    except AttributeError:
        raise UserListResponses.INVALID_SORTER_FIELD

    user_list = [UserData.model_validate(row, from_attributes=True) for row in users]
    user_count = await user_service.get_users_count()
    return PaginatedResponse(count=user_count, data=user_list)


class UserByIdResponses(Responses):
    USER_NOT_FOUND = 404, "User not found"


@users_router.get(
    "/{user_id}",
    response_model=UserData,
    responses=UserByIdResponses.get_responses(),
)
async def get_user_by_id(user_id: int, user_service: UserServiceDep) -> UserData:
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise UserByIdResponses.USER_NOT_FOUND
    return UserData.from_orm(user)


class UserDeleteResponses(Responses):
    USER_NOT_FOUND = 404, "User not found"


@users_router.delete(
    "/{user_id}",
    responses=UserDeleteResponses.get_responses(),
)
async def delete_user_by_id(user_id: int, user_service: UserServiceDep) -> str:
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise UserDeleteResponses.USER_NOT_FOUND
    await user_service.delete_user(user_id)
    return "User successfully deleted"


class UserUpdateResponses(Responses):
    USER_NOT_FOUND = 404, "User not found"


@users_router.put("/{user_id}", responses=UserUpdateResponses.get_responses())
async def update_user_by_id(user_id: int, update_user_data: UpdateUserData, user_service: UserServiceDep) -> str:
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise UserUpdateResponses.USER_NOT_FOUND
    await user_service.update_user(user_id, update_user_data.model_dump())
    return "Successfully updated"
