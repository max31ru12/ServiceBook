from pydantic import BaseModel


class Brand(BaseModel):
    id: int
    name: str


class Car(BaseModel):
    id: int
    model: str
    year: int
    brand_id: int
    brand: Brand
