from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.auth.router import (
    auth_router,
    get_reset_password_router,
    get_users_router,
    get_verify_router,
    register_router,
)
from app.config import DEV_MODE


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(register_router, prefix="/auth", tags=["auth"])
app.include_router(get_verify_router, prefix="/auth", tags=["auth"])
app.include_router(get_reset_password_router, prefix="/auth", tags=["auth"])
app.include_router(get_users_router, prefix="/users", tags=["users"])


@app.get("/")
async def root():
    return {"message": f"Hello World DEV_MODE: {DEV_MODE}"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name} "}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
