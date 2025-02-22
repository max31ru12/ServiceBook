from pydantic import BaseModel


class Brand(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True, "input_type": list}


class CarData(BaseModel):
    id: int
    model: str
    year: int
    brand_id: int

    model_config = {"from_attributes": True, "input_type": list}


class CarWithBrandData(CarData):
    brand: Brand
