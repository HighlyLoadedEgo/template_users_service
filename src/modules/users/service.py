from uuid import UUID

from src.core.auth import TokensData
from src.core.auth.common.jwt import JWTManager
from src.core.common import Service
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users import use_cases
from src.modules.users.dtos import (
    CreateUserSchema,
    FullUserSchema,
    GetUserFiltersSchema,
    LoginUserSchema,
    UpdateUserSchema,
    UsersWithPaginationSchema,
)
from src.modules.users.uow import UserUoW


class UserService(Service):
    def __init__(self, uow: UserUoW, jwt_manager: JWTManager):
        self._uow = uow
        self._jwt_manager = jwt_manager

    async def get_users(
        self, filters: GetUserFiltersSchema, pagination: PaginationSchema
    ) -> UsersWithPaginationSchema:
        return await use_cases.GetUsersUseCase(uow=self._uow)(
            filters=filters, pagination=pagination
        )

    async def check_valid_user(self, user_credentials: LoginUserSchema) -> TokensData:
        return await use_cases.CheckValidUserUseCase(
            uow=self._uow, jwt_manager=self._jwt_manager
        )(user_credentials=user_credentials)

    async def get_user_by_id(self, user_id: UUID) -> FullUserSchema:
        return await use_cases.GetUserByIdUseCase(uow=self._uow)(user_id=user_id)

    async def create_user(self, create_user_data: CreateUserSchema) -> None:
        return await use_cases.CreateUserUseCase(uow=self._uow)(
            create_user_data=create_user_data
        )

    async def update_user(self, update_user_data: UpdateUserSchema) -> None:
        await use_cases.UpdateUserUseCase(uow=self._uow)(
            update_user_data=update_user_data
        )

    async def delete_user(self, user_id: UUID) -> None:
        await use_cases.DeleteUserUseCase(uow=self._uow)(user_id=user_id)
