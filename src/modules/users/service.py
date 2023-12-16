from uuid import UUID

from src.common.interfaces.service import Service
from src.database.postgres.schemas import PaginationSchema
from src.modules.users import use_cases
from src.modules.users.schemas import (
    CreateUserSchema,
    FullUserSchema,
    GetUserFiltersSchema,
    LoginUserSchema,
    UpdateUserSchema,
    UsersWithPaginationSchema,
)
from src.modules.users.uow import UserUoW


class UserService(Service):
    def __init__(self, uow: UserUoW):
        self._uow = uow

    async def get_users(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> UsersWithPaginationSchema:
        return await use_cases.GetUsersUseCase(uow=self._uow)(
            filters=filters, pagination=pagination
        )

    async def check_valid_user(
        self, user_credentials: LoginUserSchema
    ) -> FullUserSchema:
        return await use_cases.CheckValidUserUseCase(uow=self._uow)(
            user_credentials=user_credentials
        )

    async def get_user_by_email(self, email: str) -> FullUserSchema:
        return await use_cases.GetUserByEmailUseCase(uow=self._uow)(email=email)

    async def get_user_by_username(self, username: str) -> FullUserSchema:
        return await use_cases.GetUserByUsernameUseCase(uow=self._uow)(
            username=username
        )

    async def get_user_by_id(self, user_id: UUID) -> FullUserSchema:
        return await use_cases.GetUserByIdUseCase(uow=self._uow)(user_id=user_id)

    async def create_user(self, create_user_data: CreateUserSchema) -> FullUserSchema:
        return await use_cases.CreateUserUseCase(uow=self._uow)(
            create_user_data=create_user_data
        )

    async def update_user(self, update_user_data: UpdateUserSchema) -> None:
        await use_cases.UpdateUserUseCase(uow=self._uow)(
            update_user_data=update_user_data
        )

    async def delete_user(self, user_id: UUID) -> None:
        await use_cases.DeleteUserUseCase(uow=self._uow)(user_id=user_id)
