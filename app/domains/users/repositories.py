from app.core.utils.base_repository import BaseAsyncSQLAlchemyRepository
from app.domains.users.models import User


class UserRepository(BaseAsyncSQLAlchemyRepository[User]):
    model = User
