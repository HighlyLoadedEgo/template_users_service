from abc import (
    ABC,
    abstractmethod,
)

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.dtos import (
    FullUserSchema,
    GetUserFiltersSchema,
)


class UserReader(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def get_users(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> list[FullUserSchema]:
        """Get users from database by filters."""

    @abstractmethod
    async def get_users_count(self) -> int | None:
        """Get count of users."""

    @abstractmethod
    async def get_user_by_username(self, username: str) -> FullUserSchema | None:
        """Get user by username."""
