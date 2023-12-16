from src.common.interfaces.use_case import UseCase
from src.database.postgres.schemas import PaginationSchema
from src.modules.users.schemas import (
    GetUserFiltersSchema,
    UsersWithPaginationSchema,
)
from src.modules.users.uow import UserUoW


class GetUsersUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> UsersWithPaginationSchema:
        """Get all users with pagination and filters."""
        users = await self._uow.user_reader.get_users(
            filters=filters, pagination=pagination
        )

        total_count_of_users = await self._uow.user_reader.get_users_count()

        return UsersWithPaginationSchema.model_validate(
            dict(users=users, total=total_count_of_users, **pagination.model_dump())
        )
