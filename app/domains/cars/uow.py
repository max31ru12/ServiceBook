from app.core.utils.unit_of_work import SQLAlchemyUnitOfWork
from app.domains.cars.repositories import BrandRepository, CarRepository


class CarsUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self):
        super().__init__()
        self.car_repository = CarRepository(self._session)
        self.brand_repository = BrandRepository(self._session)
