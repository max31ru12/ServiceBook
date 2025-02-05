from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):

    username: str
    password: str

    model_config = {"from_attributes": True}


class UserData(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str | None
    last_name: str | None
    is_admin: bool
    is_super_user: bool

    model_config = {"from_attributes": True}


class LoginForm(BaseModel):
    username: str
    password: str = Field(min_length=5, max_length=50)


class AccessToken(BaseModel):
    access_token: str
    type: str = "bearer"


class JWTTokenResponse(AccessToken):
    refresh_token: str | None
