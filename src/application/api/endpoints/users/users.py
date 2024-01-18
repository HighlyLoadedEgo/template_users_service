import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from src.application.api.schemas.response_schemas.base_responses import (
    ErrorResponse,
    OkResponse,
)
from src.application.di.providers.users.stubs import get_service_stub
from src.core.auth import (
    Roles,
    UserPayload,
)
from src.core.auth.common.jwt import JWTManager
from src.core.auth.exceptions import InvalidTokenException
from src.core.auth.permission import CheckPermission
from src.core.auth.stubs import jwt_manager_stub
from src.core.common.constants import Empty
from src.core.database.postgres.constants import SortOrder
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users import UserService
from src.modules.users.dtos import (
    CreateUserSchema,
    GetUserFiltersSchema,
    LoginUserSchema,
    UpdateUserSchema,
)
from src.modules.users.exceptions import (
    IncorrectUserCredentialsException,
    UserDataIsExistException,
    UserDoesNotExistException,
)

from ...schemas.request_schemas import (
    CreateUserRequestSchema,
    LoginUserRequestSchema,
    UpdateUserRequestSchema,
)
from ...schemas.response_schemas import (
    FullUserResponseSchema,
    TokensDataResponse,
    UsersResponseSchema,
)

user_router = APIRouter(prefix="/users", tags=["User Endpoints"])


@user_router.post(
    "/login",
    response_model=OkResponse[TokensDataResponse],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[TokensDataResponse]},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse[IncorrectUserCredentialsException]
        },
    },
)
async def login(
    login_data: LoginUserRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    tokens = await user_service.check_valid_user(
        user_credentials=LoginUserSchema(**login_data.model_dump())
    )

    return OkResponse(result=tokens)


@user_router.post(
    "/refresh_token",
    response_model=OkResponse[TokensDataResponse],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[TokensDataResponse]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[InvalidTokenException]},
    },
)
async def refresh_token(
    jwt_manager: Annotated[JWTManager, Depends(jwt_manager_stub)],
    auth_data: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
):
    tokens = jwt_manager.refresh_tokens(token=auth_data.credentials)

    return OkResponse(result=tokens)


@user_router.get(
    "",
    response_model=OkResponse[UsersResponseSchema],
    responses={status.HTTP_200_OK: {"model": OkResponse[UsersResponseSchema]}},
)
async def get_users(
    user_service: Annotated[UserService, Depends(get_service_stub)],
    username: Annotated[str | Empty, Query()] = Empty.UNSET,
    deleted: Annotated[bool | Empty, Query()] = Empty.UNSET,
    role: Annotated[Roles | Empty, Query()] = Empty.UNSET,
    order: Annotated[SortOrder, Query()] = SortOrder.ASC,
    limit: Annotated[int, Query(ge=0, le=1000)] = 1000,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    users = await user_service.get_users(
        filters=GetUserFiltersSchema(role=role, deleted=deleted, username=username),
        pagination=PaginationSchema(offset=offset, limit=limit, order=order),
    )

    return OkResponse(result=users)


@user_router.get(
    "/{user_id}",
    response_model=OkResponse[FullUserResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[FullUserResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserDoesNotExistException]},
    },
)
async def get_user(
    user_id: Annotated[uuid.UUID, Path()],
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    user = await user_service.get_user_by_id(user_id=user_id)

    return OkResponse(result=user)


@user_router.get(
    "/profile",
    response_model=OkResponse[FullUserResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[FullUserResponseSchema]},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse[UserDoesNotExistException]},
    },
)
async def get_profile(
    token_payload: Annotated[CheckPermission, Depends(CheckPermission())],
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    user_payload: UserPayload = token_payload.get_user_payload()

    user = await user_service.get_user_by_id(user_id=user_payload.id)

    return OkResponse(result=user)


@user_router.patch(
    "",
    response_model=OkResponse[None],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[None]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[InvalidTokenException]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserDataIsExistException]},
    },
)
async def update_user(
    update_user_data: UpdateUserRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
    token_payload: Annotated[CheckPermission, Depends(CheckPermission())],
):
    user_data: UserPayload = token_payload.get_user_payload()
    await user_service.update_user(
        update_user_data=UpdateUserSchema(
            user_id=user_data.id, **update_user_data.model_dump()
        )
    )

    return OkResponse(message="Updated successfully!")


@user_router.post(
    "",
    response_model=OkResponse[None],
    responses={
        status.HTTP_201_CREATED: {"model": OkResponse[None]},
        status.HTTP_409_CONFLICT: {"model": ErrorResponse[UserDataIsExistException]},
    },
)
async def create_user(
    create_user_data: CreateUserRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
):
    await user_service.create_user(
        create_user_data=CreateUserSchema(**create_user_data.model_dump())
    )

    return OkResponse(message="Done!")


@user_router.delete(
    "",
    response_model=OkResponse[None],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[None]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[InvalidTokenException]},
    },
)
async def delete_user(
    user_service: Annotated[UserService, Depends(get_service_stub)],
    token_payload: Annotated[CheckPermission, Depends(CheckPermission())],
):
    user_payload: UserPayload = token_payload.get_user_payload()
    await user_service.delete_user(user_id=user_payload.id)

    return OkResponse(message="User was deleted!")
