from uuid import UUID

from sqlalchemy import (
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError

from src.core.common.constants import Empty
from src.modules.users.common.repository import UserRepository
from src.modules.users.exceptions import (
    UserDoesNotExistException,
    UserIsExistException,
)
from src.modules.users.models import User
from src.modules.users.schemas import (
    CreateUserSchema,
    UpdateUserSchema,
)


class UserRepositoryImpl(UserRepository):
    async def create_user(self, create_user_data: CreateUserSchema) -> User | None:
        """Create a new user in database."""
        optional_create_data = dict()
        if create_user_data.email:
            optional_create_data.update({"email": create_user_data.email})
        if create_user_data.phone:
            optional_create_data.update({"phone": create_user_data.phone})

        stmt = (
            insert(User)
            .values(
                username=create_user_data.username,
                hashed_password=create_user_data.password,
                **optional_create_data,
            )
            .returning(User)
        )

        try:
            result = await self._session.scalar(stmt)
            await self._session.flush()
        except IntegrityError as err:
            # TODO переделать обработку ошибок
            raise UserIsExistException() from err

        return result

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        """Get user by id from database."""
        stmt = select(User).where(User.id == user_id)

        result = await self._session.scalar(stmt)

        if not result:
            raise UserDoesNotExistException()

        return result

    async def update_user(self, update_user_data: UpdateUserSchema) -> User | None:
        """Update user in database."""
        update_data = {
            key: value
            for key, value in update_user_data.model_dump().items()
            if value is not Empty.UNSET and key != "user_id"
        }
        stmt = (
            update(User)
            .values(**update_data)
            .where(User.id == update_user_data.user_id)
            .returning(User)
        )
        try:
            result = await self._session.scalar(stmt)
        except IntegrityError as err:
            raise UserIsExistException(invalid_data=list(update_data.keys())) from err

        return result

    async def delete_user(self, user_id: UUID) -> UUID | None:
        """Delete user from database."""
        stmt = (
            update(User)
            .values(is_deleted=True)
            .where(User.id == user_id)
            .returning(User.id)
        )
        result = await self._session.scalar(stmt)

        return result
