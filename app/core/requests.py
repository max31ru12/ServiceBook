from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int
    page_size: int


def get_pagination_params(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = (Query(10, ge=1, le=100, description="Размер страницы")),
) -> PaginationParams:
    return PaginationParams(page=page, page_size=page_size)


PaginationParamsDep = Annotated[PaginationParams, Depends(get_pagination_params)]
OrderingDep = Annotated[str | None, Query(description="Параметр сортировки")]
