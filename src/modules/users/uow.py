from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import SqlAlchemyUow
from src.modules.users.common.reader import UserReader
from src.modules.users.common.repository import UserRepository


class UserUoW(SqlAlchemyUow):
    def __init__(
        self,
        user_repository: type[UserRepository],
        user_reader: type[UserReader],
        session: AsyncSession,
    ) -> None:
        self.user_repository = user_repository(session=session)
        self.user_reader = user_reader(session=session)
        super().__init__(session=session)
