from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str

    model_config = {"from_attributes": True}


class UserData(CreateUser):
    first_name: str | None
    last_name: str | None
    is_admin: bool
    is_super_user: bool
    id: int


class LoginForm(BaseModel):
    username: str
    password: str = Field(min_length=5, max_length=50)


class JWTTokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None
