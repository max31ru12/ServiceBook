from fastapi import APIRouter

from app.users.schemas import LoginForm

router = APIRouter(prefix="/users")


@router.post("/login")
async def login(data: LoginForm):

    return data
