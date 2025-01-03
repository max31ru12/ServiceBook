from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy

from app.auth.models import AccessToken, User
from app.config import settings

bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(
        AccessToken.get_access_token_db
    ),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME
    )


auth_backend = AuthenticationBackend(
    name="token",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(User.get_user_db)):
    yield UserManager(user_db)
