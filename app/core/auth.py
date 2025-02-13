from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES
    )
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encode_jwt


def create_refresh_token(data: dict, remember_me: bool = False) -> str:
    data_to_encode = data.copy()
    if remember_me:
        lifetime = timedelta(days=settings.REFRESH_TOKEN_LIFETIME_DAYS)
    else:
        lifetime = timedelta(days=settings.REFRESH_TOKEN_LIFETIME_DAYS_NOT_REMEMBER)
    expire = datetime.now() + lifetime
    data_to_encode.update({"exp": expire})
    refresh_token = jwt.encode(
        data_to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return refresh_token
