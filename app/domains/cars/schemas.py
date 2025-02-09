from pydantic import BaseModel


class Brand(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class Car(BaseModel):
    id: int
    model: str
    year: int
    brand_id: int
    brand: Brand

    model_config = {"from_attributes": True, "input_type": list}
