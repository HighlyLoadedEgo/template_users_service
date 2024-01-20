from sqlalchemy import (
    ScalarResult,
    func,
    select,
)

from src.core.common.constants import Empty
from src.core.database.postgres.constants import SortOrder
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.common.reader import UserReader
from src.modules.users.dtos import GetUserFiltersSchema
from src.modules.users.models import Users


class UserReaderImpl(UserReader):
    async def get_users(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> ScalarResult[Users]:
        """Get users from database by filters."""
        stmt = select(Users)

        filter_scope = list()
        if filters.deleted is not Empty.UNSET:
            filter_scope.append(Users.is_deleted.is_(filters.deleted))
        if filters.role is not Empty.UNSET:
            filter_scope.append(Users.role == filters.role)  # type: ignore
        if filters.username is not Empty.UNSET:
            filter_scope.append(Users.username == filters.username)  # type: ignore

        stmt = stmt.where(*filter_scope)

        if pagination.order == SortOrder.ASC:
            stmt.order_by(Users.username.asc())
        else:
            stmt.order_by(Users.username.desc())

        stmt = stmt.limit(pagination.limit).offset(pagination.limit * pagination.offset)
        result = await self._session.scalars(stmt)

        return result

    async def get_users_count(self) -> int | None:
        """Get users count."""
        stmt = select(func.count(1)).select_from(Users)  # type: ignore

        result = await self._session.scalar(stmt)

        return result

    async def get_user_by_username(self, username: str) -> Users | None:
        """Get user by username."""

        stmt = select(Users).where(Users.username == username)

        result = await self._session.scalar(stmt)

        return result
