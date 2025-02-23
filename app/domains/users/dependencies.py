from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from jose import JWTError, jwt
from starlette import status

from app.core.config import settings
from app.domains.users.models import User
from app.domains.users.services import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login/swagger", scheme_name="Bearer")
refresh_token_cookie = APIKeyCookie(name="refresh_token", auto_error=True)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await UserService().get_user_by_kwargs(username=username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return user


def verify_refresh_token(refresh_token: Annotated[str, Depends(refresh_token_cookie)]) -> dict | None:
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is invalid")


def get_user_service() -> UserService:
    return UserService()


RefreshTokenDep = Annotated[str, Depends(verify_refresh_token)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
