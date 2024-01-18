from uuid import UUID

from asyncpg import UniqueViolationError  # type: ignore
from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.exc import DBAPIError

from src.core.common.constants import Empty
from src.core.database.exceptions import RepositoryException
from src.modules.users.common.repository import UserRepository
from src.modules.users.dtos import (
    CreateUserSchema,
    UpdateUserSchema,
)
from src.modules.users.exceptions import UserDataIsExistException
from src.modules.users.models import Users


class UserRepositoryImpl(UserRepository):
    async def create_user(self, create_user_data: CreateUserSchema) -> None:
        """Create a new user in database."""
        optional_create_data = dict()
        if create_user_data.email:
            optional_create_data.update({"email": create_user_data.email})
        if create_user_data.phone:
            optional_create_data.update({"phone": create_user_data.phone})

        stmt = (
            insert(Users)
            .values(
                username=create_user_data.username,
                hashed_password=create_user_data.password,
                **optional_create_data,
            )
            .returning(Users)
        )

        try:
            await self._session.scalar(stmt)
        except DBAPIError as err:
            self._parse_error(err=err, data=create_user_data)

    async def get_user_by_id(self, user_id: UUID) -> Users | None:
        """Get user by id from database."""
        stmt = select(Users).where(Users.id == user_id)

        result = await self._session.scalar(stmt)

        return result

    async def update_user(self, update_user_data: UpdateUserSchema) -> None:
        """Update user in database."""
        update_data = {
            key: value
            for key, value in update_user_data.model_dump().items()
            if value is not Empty.UNSET and key != "user_id"
        }
        stmt = (
            update(Users)
            .values(**update_data)
            .where(Users.id == update_user_data.user_id)
            .returning(Users)
        )
        try:
            await self._session.scalar(stmt)
        except DBAPIError as err:
            self._parse_error(err=err, data=update_user_data)

    async def delete_user(self, user_id: UUID) -> UUID | None:
        """Delete user from database."""
        stmt = (
            update(Users)
            .values(is_deleted=True)
            .where(Users.id == user_id)
            .returning(Users.id)
        )
        result = await self._session.scalar(stmt)

        return result

    @staticmethod
    def _parse_error(
        err: DBAPIError, data: UpdateUserSchema | CreateUserSchema
    ) -> None:
        """Parse error and raise exception with info."""

        error = err.__cause__.__cause__.__class__  # type: ignore

        if error == UniqueViolationError:
            match data:
                case CreateUserSchema() | UpdateUserSchema():
                    raise UserDataIsExistException(
                        creation_data=err.args[0].split(":  ")[-1]
                    )
        else:
            raise RepositoryException() from err
