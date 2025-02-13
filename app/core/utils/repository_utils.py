from typing import Any

from sqlalchemy import Select


def paginate_stmt(stmt: Select | Select[tuple[Any]], limit: int, offset: int):
    stmt = stmt.limit(limit).offset(offset)
    return stmt
