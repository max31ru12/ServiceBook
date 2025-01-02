from fastapi_users import FastAPIUsers

from app.auth.models import User
from app.auth.schemas import UserRead, UserCreate, UserUpdate
from app.auth.config import get_user_manager, auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
get_verify_router = fastapi_users.get_verify_router(UserRead)
get_reset_password_router = fastapi_users.get_reset_password_router()
get_users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
