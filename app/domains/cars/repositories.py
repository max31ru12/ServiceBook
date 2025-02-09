from app.core.base_repository import BaseAsyncSQLAlchemyRepository
from app.domains.cars.models import Brand, Car


class BrandRepository(BaseAsyncSQLAlchemyRepository):
    model = Brand


class CarRepository(BaseAsyncSQLAlchemyRepository):
    model = Car
