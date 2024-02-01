from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from src.application.api.schemas.response_schemas.base_responses import (
    ErrorResponse,
    OkResponse,
)
from src.application.di.providers.users.stubs import get_service_stub
from src.core.auth import Roles
from src.core.auth.exceptions import (
    AccessDeniedException,
    InvalidTokenException,
)
from src.core.auth.permission import CheckPermission
from src.modules.users import UserService
from src.modules.users.dtos import UpdateUserSchema

from ...schemas.request_schemas import UpdateUserRoleRequestSchema

admin_router = APIRouter(prefix="/admin/users", tags=["Users Admin Endpoints"])


@admin_router.patch(
    "/role/",
    response_model=OkResponse[None],
    responses={
        status.HTTP_200_OK: {"model": OkResponse[None]},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse[InvalidTokenException]},
        status.HTTP_403_FORBIDDEN: {"model": ErrorResponse[AccessDeniedException]},
    },
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CheckPermission(permission_list=[Roles.ADMIN]))],
)
async def update_user_role(
    update_user_role_data: UpdateUserRoleRequestSchema,
    user_service: Annotated[UserService, Depends(get_service_stub)],
) -> OkResponse[dict]:
    await user_service.update_user(
        update_user_data=UpdateUserSchema(**update_user_role_data.model_dump())
    )

    return OkResponse()
