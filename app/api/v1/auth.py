from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from app.core.auth import create_access_token, verify_password
from app.core.responses import Responses
from app.domains.users.dependencies import CurrentUserDep, UserServiceDep
from app.domains.users.schemas import (
    AccessToken,
    CreateUser,
    JWTTokenResponse,
    LoginForm,
    UserData,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterResponses(Responses):
    USERNAME_ALREADY_IN_USE = 409, "User with provided username is already exists"


@auth_router.post(
    "/register",
    response_model=UserData,
    status_code=201,
    responses=RegisterResponses.get_responses(),
)
async def register_user(
    user_data: CreateUser, user_service: UserServiceDep
) -> UserData:

    if (await user_service.get_user_by_kwargs(username=user_data.username)) is not None:
        raise HTTPException(
            status_code=409, detail="User with provided username is already exists"
        )

    new_user = await user_service.create_user(user_data)

    return UserData.from_orm(new_user)


class LoginResponses(Responses):
    INVALID_CREDENTIALS = 401, "Invalid username or password"
    USER_NOT_FOUND = 404, "User not found"


@auth_router.post(
    "/login",
    response_model=JWTTokenResponse,
    responses=LoginResponses.get_responses(),
)
async def login(
    response: Response, data: LoginForm, user_service: UserServiceDep
) -> JWTTokenResponse:

    user = await user_service.get_user_by_kwargs(username=data.username)

    if user is None:
        raise HTTPException(status_code=404, detail="There is no such user")

    if not verify_password(data.password, user.password):
        raise LoginResponses.INVALID_CREDENTIALS
        # raise HTTPException(status_code=401, detail="Wrong credentials")

    access_token = create_access_token({"sub": user.username})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return JWTTokenResponse(access_token=access_token, refresh_token=None)


@auth_router.post("/refresh", response_model=AccessToken)
async def refresh_access_token() -> AccessToken:
    return {"access_token": "access-token"}


@auth_router.post("/logout")
async def logout(response: Response, user: CurrentUserDep) -> str:
    response.delete_cookie("users_access_token")
    return "Successfully logged out"
