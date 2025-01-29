from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.core.auth import create_access_token, verify_password
from app.core.setup_db import session_getter
from app.domains.users.dependencies import CurrentUser
from app.domains.users.schemas import CreateUser, JWTTokenResponse, LoginForm, UserData
from app.domains.users.service import UserService

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
async def register_user(
    user_data: CreateUser, session=Depends(session_getter)
) -> UserData:

    if (
        await UserService(session).get_user_by_kwargs(email=user_data.email)
    ) is not None:
        raise HTTPException(
            status_code=409, detail="User with provided email is already exists"
        )

    if (
        await UserService(session).get_user_by_kwargs(username=user_data.username)
    ) is not None:
        raise HTTPException(
            status_code=409, detail="User with provided username is already exists"
        )

    new_user = await UserService(session).create_user(user_data)

    return UserData.from_orm(new_user)


@auth_router.post("/login")
async def login(
    response: Response, data: LoginForm, session=Depends(session_getter)
) -> JWTTokenResponse:

    user = await UserService(session).get_user_by_kwargs(username=data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="There is no such user")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong credentials")

    access_token = create_access_token({"sub": data.username})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return JWTTokenResponse(access_token=access_token, refresh_token=None)


@auth_router.post("/logout")
async def logout(response: Response, user: CurrentUser) -> str:
    response.delete_cookie("users_access_token")
    return "Successfully logged out"
