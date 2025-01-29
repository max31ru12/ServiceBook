from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    password: str


class UpdateUser(CreateUser):
    first_name: str
    last_name: str
    is_admin: bool
    is_super_user: bool


class UserData(UpdateUser):
    id: int


class LoginForm(BaseModel):
    username: str
    password: str


class JWTTokenResponse(BaseModel):
    token: str
