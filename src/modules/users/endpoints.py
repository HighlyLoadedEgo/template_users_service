import uuid

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from src.core.auth import Roles
from src.core.common.constants import Empty
from src.core.common.schemas.base_responses import SuccessResponse
from src.core.database.postgres.constants import SortOrder
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users import UserService
from src.modules.users.schemas import (
    CreateUserSchema,
    GetUserFiltersSchema,
    LoginUserSchema,
)
from src.modules.users.schemas.requests_schemas import (
    CreateUserRequestSchema,
    LoginUserRequestSchema,
)
from src.modules.users.schemas.responses_schemas import (
    FullUserResponseSchema,
    UsersResponseSchema,
)
from src.modules.users.stubs import get_service_stub

user_routers = APIRouter(prefix="/users", tags=["User Endpoints"])


@user_routers.get("", response_model=UsersResponseSchema)
async def get_users(
    deleted: bool
    | Empty = Query(default=Empty.UNSET, description="Filter users by deleted status"),
    role: Roles
    | Empty = Query(default=Empty.UNSET, description="Filter users by role"),
    offset: int
    | Empty = Query(default=Empty.UNSET, description="Pagination with offset"),
    limit: int
    | Empty = Query(default=Empty.UNSET, description="Pagination with limit"),
    order: SortOrder = Query(
        default=SortOrder.ASC, description="Pagination with order"
    ),
    user_service: UserService = Depends(get_service_stub),
):
    return await user_service.get_users(
        filters=GetUserFiltersSchema(role=role, deleted=deleted),
        pagination=PaginationSchema(offset=offset, limit=limit, order=order),
    )


@user_routers.post("/login", response_model=FullUserResponseSchema)
async def login(
    login_data: LoginUserRequestSchema,
    user_service: UserService = Depends(get_service_stub),
):
    return await user_service.check_valid_user(
        user_credentials=LoginUserSchema(**login_data.model_dump())
    )


@user_routers.get("/{user_id}", response_model=FullUserResponseSchema)
async def get_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_service_stub)
):
    return await user_service.get_user_by_id(user_id=user_id)


@user_routers.patch("/{user_id}")
async def update_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_service_stub)
):
    pass


@user_routers.patch("/{user_id}/role")
async def update_user_role(
    user_id: uuid.UUID, user_service: UserService = Depends(get_service_stub)
):
    pass


@user_routers.post("", response_model=FullUserResponseSchema)
async def create_user(
    create_user_data: CreateUserRequestSchema,
    user_service: UserService = Depends(get_service_stub),
):
    return await user_service.create_user(
        create_user_data=CreateUserSchema(**create_user_data.model_dump())
    )


@user_routers.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_service_stub)
):
    await user_service.delete_user(user_id=user_id)

    return SuccessResponse(message="User was deleted!", data=dict(user_id=user_id))
