from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.core.setup_db import session_getter
from app.domains.users.models import User
from app.domains.users.service import UserService

access_token_cookie = APIKeyCookie(name="users_access_token", auto_error=True)
refresh_token_cookie = APIKeyCookie(name="users_refresh_token", auto_error=True)


async def get_current_user(
    token: str = Depends(access_token_cookie),
    session: AsyncSession = Depends(session_getter),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invakid token"
        )

    user = await UserService(session).get_user_by_kwargs(username=username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    return user


def verify_refresh_token(
    refresh_token: Annotated[str, Depends(refresh_token_cookie)]
) -> dict | None:
    try:
        payload = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is invalid"
        )


RefreshTokenDep = Annotated[str, Depends(verify_refresh_token)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(UserService)]
