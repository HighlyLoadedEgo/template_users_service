from abc import (
    ABC,
    abstractmethod,
)

from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.models import User
from src.modules.users.schemas import GetUserFiltersSchema


class UserReader(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        """Get user by username from database."""

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email from database."""

    @abstractmethod
    async def get_user_by_phone(self, phone: str) -> User | None:
        """Get user by phone from database."""

    @abstractmethod
    async def get_users(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> ScalarResult[User]:
        """Get users from database by filters."""

    @abstractmethod
    async def get_users_count(self) -> int | None:
        """Get count of users."""
