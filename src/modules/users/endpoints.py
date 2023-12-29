import uuid

from fastapi import (
    APIRouter,
    Depends,
)

from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users import UserService
from src.modules.users.schemas import GetUserFiltersSchema
from src.modules.users.schemas.responses_schemas import (
    UserResponseSchema,
    UsersResponseSchema,
)
from src.modules.users.stubs import get_service_stub

user_routers = APIRouter(prefix="/users", tags=["User Endpoints"])


@user_routers.get("", response_model=UsersResponseSchema)
async def get_users(
    filters: GetUserFiltersSchema = Depends(),
    pagination: PaginationSchema = Depends(),
    user_service: UserService = Depends(get_service_stub),
):
    return await user_service.get_users(filters=filters, pagination=pagination)


@user_routers.get("/{user_id}", response_model=UserResponseSchema)
async def get_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_service_stub)
):
    return await user_service.get_user_by_id(user_id=user_id)


@user_routers.patch("/{user_id}")
async def update_user():
    pass


@user_routers.post("")
async def create_user():
    pass


@user_routers.delete("/{user_id}")
async def delete_user():
    pass
