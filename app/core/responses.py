from typing import Any, Generic, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel


class Responses:
    @classmethod
    def get_responses(cls) -> dict[int | str, dict[str, Any]] | None:
        responses_dict = {}
        for attr in dir(cls):
            if not attr.startswith("__") and not callable(getattr(cls, attr)):
                status_code, detail = getattr(cls, attr)
                responses_dict[status_code] = {
                    "description": attr.replace("_", " "),
                    "content": {"application/json": {"example": {"detail": detail}}},
                }
                setattr(
                    cls, attr, HTTPException(status_code=status_code, detail=detail)
                )
        return responses_dict or None


DataModel = TypeVar("DataModel", bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[DataModel]):
    count: int
    data: list[DataModel]
