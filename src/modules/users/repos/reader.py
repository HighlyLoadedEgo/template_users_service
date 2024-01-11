from sqlalchemy import (
    ScalarResult,
    func,
    select,
)

from src.core.common.constants import Empty
from src.core.database.postgres.constants import SortOrder
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.common.reader import UserReader
from src.modules.users.exceptions import UserDoesNotExistException
from src.modules.users.models import User
from src.modules.users.schemas import GetUserFiltersSchema


class UserReaderImpl(UserReader):
    async def get_users(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> ScalarResult[User]:
        """Get users from database by filters."""
        stmt = select(User)

        filter_scope = list()
        if filters.deleted is not Empty.UNSET:
            filter_scope.append(User.is_deleted.is_(filters.deleted))
        if filters.role is not Empty.UNSET:
            filter_scope.append(User.role == filters.role)  # type: ignore

        stmt = stmt.where(*filter_scope)

        if pagination.order is not Empty.UNSET:
            if pagination.order == SortOrder.ASC:
                stmt.order_by(User.username.asc())
            else:
                stmt.order_by(User.username.desc())

        stmt = stmt.limit(pagination.limit).offset(pagination.offset)
        result = await self._session.scalars(stmt)

        return result

    async def get_users_count(self) -> int | None:
        """Get users count."""
        stmt = select(func.count(1)).select_from(User)

        result = await self._session.scalar(stmt)

        return result

    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username from database."""
        stmt = select(User).where(User.username == username)

        result = await self._session.scalar(stmt)

        if not result:
            raise UserDoesNotExistException()

        return result

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email from database."""
        stmt = select(User).where(User.email == email)

        result = await self._session.scalar(stmt)

        if not result:
            raise UserDoesNotExistException()

        return result

    async def get_user_by_phone(self, phone: str) -> User | None:
        """Get user by phone from database."""
        stmt = select(User).where(User.phone == phone)

        result = await self._session.scalar(stmt)

        if not result:
            raise UserDoesNotExistException()

        return result
