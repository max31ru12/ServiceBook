from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.setup_db import Base


class User(Base):

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)

    is_admin: Mapped[bool] = mapped_column(
        default=False, server_default=text("false"), nullable=False
    )
    is_super_user: Mapped[bool] = mapped_column(
        default=False, server_default=text("false"), nullable=False
    )
