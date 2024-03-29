import structlog

from src.core.common.interfaces.use_case import UseCase
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.dtos import (
    FullUserSchema,
    GetUserFiltersSchema,
    UsersWithPaginationSchema,
)
from src.modules.users.uow import UserUoW

logger = structlog.stdlib.get_logger(__name__)


class GetUsersUseCase(UseCase):
    def __init__(self, uow: UserUoW) -> None:
        self._uow = uow

    async def __call__(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> UsersWithPaginationSchema:
        """Get all users with pagination and filters."""
        users: list[FullUserSchema] = await self._uow.user_reader.get_users(
            filters=filters, pagination=pagination
        )

        total_count_of_users = await self._uow.user_reader.get_users_count()

        logger.debug(
            "Get users",
            users=users,
            total_count=total_count_of_users,
            pagination=pagination,
            filters=filters,
        )

        return UsersWithPaginationSchema(
            users=users,
            total=total_count_of_users,
            **pagination.model_dump(),
        )
