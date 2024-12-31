from fastapi_users import FastAPIUsers

from app.models import User
from app.schemas.user import UserRead, UserCreate
from app.utils.auth import get_user_manager, auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
