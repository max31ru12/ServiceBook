from pydantic import BaseModel


class LoginForm(BaseModel):
    username: str
    password: str


class JWTTokenResponse(BaseModel):
    token: str
