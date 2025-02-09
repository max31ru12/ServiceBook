from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.setup_db import Base


class Brand(Base):
    __tablename__ = "brand"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    cars: Mapped[list["Car"]] = relationship(back_populates="brand")


class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()

    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    brand: Mapped["Brand"] = relationship(back_populates="cars")
