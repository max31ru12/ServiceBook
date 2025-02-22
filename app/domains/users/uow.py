from app.core.utils.unit_of_work import SQLAlchemyUnitOfWork
from app.domains.users.repositories import UserRepository


class UsersUnitOfWork(SQLAlchemyUnitOfWork):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository(self._session)
