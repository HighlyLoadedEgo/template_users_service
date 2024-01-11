import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from src.core.auth import Roles
from src.core.auth.common.jwt import JWTManager
from src.core.auth.permission import CheckPermission
from src.core.auth.stubs import jwt_manager_stub
from src.core.common.constants import Empty
from src.core.common.schemas.base_responses import OkResponse
from src.core.database.postgres.constants import SortOrder
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users import UserService
from src.modules.users.schemas import (
    CreateUserSchema,
    GetUserFiltersSchema,
    LoginUserSchema,
    UpdateUserSchema,
)
from src.modules.users.schemas.requests_schemas import (
    CreateUserRequestSchema,
    LoginUserRequestSchema,
    UpdateUserRequestSchema,
    UpdateUserRoleRequestSchema,
)
from src.modules.users.schemas.responses_schemas import (
    FullUserResponseSchema,
    TokensDataResponse,
    UsersResponseSchema,
)
from src.modules.users.stubs import get_service_stub

user_routers = APIRouter(prefix="/users", tags=["User Endpoints"])


@user_routers.get("/", response_model=OkResponse[UsersResponseSchema])
async def get_users(
    user_service: Annotated[UserService, Depends(get_service_stub)],
    deleted: Annotated[bool | Empty, Query()] = Empty.UNSET,
    role: Annotated[Roles | Empty, Query()] = Empty.UNSET,
    order: Annotated[SortOrder, Query()] = SortOrder.ASC,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    users = await user_service.get_users(
        filters=GetUserFiltersSchema(role=role, deleted=deleted),
        pagination=PaginationSchema(offset=offset, limit=limit, order=order),
    )

    return OkResponse(result=users)


@user_routers.get("/me", response_model=OkResponse[FullUserResponseSchema])
async def get_me(
    token_payload: Annotated[CheckPermission, Depends(CheckPermission())],
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    user_id = token_payload.get_user_payload().id

    user = await user_service.get_user_by_id(user_id=user_id)

    return OkResponse(result=user)


@user_routers.post("/login", response_model=OkResponse[TokensDataResponse])
async def login(
    login_data: LoginUserRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    tokens = await user_service.check_valid_user(
        user_credentials=LoginUserSchema(**login_data.model_dump())
    )

    return OkResponse(result=tokens)


@user_routers.post("/refresh_token", response_model=OkResponse[TokensDataResponse])
async def refresh_token(
    jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
    auth_data: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    tokens = jwt_manager.refresh_tokens(token=auth_data.credentials)

    return OkResponse(result=tokens)


@user_routers.get(
    "/{user_id}/user_id", response_model=OkResponse[FullUserResponseSchema]
)
async def get_user(
    user_id: uuid.UUID,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    user = await user_service.get_user_by_id(user_id=user_id)

    return OkResponse(result=user)


@user_routers.patch(
    "/{user_id}",
    response_model=OkResponse[dict],
    dependencies=[Depends(CheckPermission())],
)
async def update_user(
    user_id: uuid.UUID,
    update_user_data: UpdateUserRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
) -> OkResponse[dict]:
    await user_service.update_user(
        update_user_data=UpdateUserSchema(
            user_id=user_id, **update_user_data.model_dump()
        )
    )

    return OkResponse(message="Updated successfully!", result=dict(user_id=user_id))


@user_routers.patch(
    "/{user_id}/role",
    response_model=OkResponse[dict],
    dependencies=[Depends(CheckPermission(permission_list=[Roles.ADMIN]))],
)
async def update_user_role(
    user_id: uuid.UUID,
    update_user_role_data: UpdateUserRoleRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
) -> OkResponse[dict]:
    await user_service.update_user(
        update_user_data=UpdateUserSchema(
            user_id=user_id, **update_user_role_data.model_dump()
        )
    )

    return OkResponse(
        message="Role updated successfully!", result=dict(user_id=user_id)
    )


@user_routers.post("/", response_model=OkResponse[FullUserResponseSchema])
async def create_user(
    create_user_data: CreateUserRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    await user_service.create_user(
        create_user_data=CreateUserSchema(**create_user_data.model_dump())
    )

    return OkResponse(message="Done!")


@user_routers.delete(
    "/{user_id}",
    response_model=OkResponse[dict],
    dependencies=[Depends(CheckPermission(permission_list=[Roles.USER]))],
)
async def delete_user(
    user_id: uuid.UUID,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    await user_service.delete_user(user_id=user_id)

    return OkResponse(message="User was deleted!", result=dict(user_id=user_id))


@user_routers.get("/@{username}", response_model=OkResponse[FullUserResponseSchema])
async def get_user_by_username(
    username: Annotated[str, Path()],
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    user = await user_service.get_user_by_username(username=username)

    return OkResponse(result=user)


@user_routers.get("/{email}", response_model=OkResponse[FullUserResponseSchema])
async def get_user_by_email(
    email: str,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    user = await user_service.get_user_by_email(email=email)

    return OkResponse(result=user)
