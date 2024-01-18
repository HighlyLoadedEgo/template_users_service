from abc import (
    ABC,
    abstractmethod,
)
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.users.dtos import (
    CreateUserSchema,
    UpdateUserSchema,
)
from src.modules.users.models import Users


class UserRepository(ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @abstractmethod
    async def create_user(self, create_user_data: CreateUserSchema) -> Users | None:
        """Create a new user in database."""

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Users | None:
        """Get user by id from database."""

    @abstractmethod
    async def update_user(self, update_user_data: UpdateUserSchema) -> Users | None:
        """Update user in database."""

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> UUID | None:
        """Delete user from database."""
