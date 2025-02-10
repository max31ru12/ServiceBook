from typing import Any

from sqlalchemy import Select, desc


def paginate_stmt(stmt: Select | Select[tuple[Any]], limit: int, offset: int):
    stmt = stmt.limit(limit).offset(offset)
    return stmt


def order_stmt(stmt: Select | Select[tuple[Any]], sort_by: str):
    sorter = desc(sort_by.strip("-")) if sort_by.startswith("-") else sort_by.strip("-")
    stmt = stmt.order_by(sorter)
    return stmt
