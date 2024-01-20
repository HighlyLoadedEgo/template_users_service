import uuid

from pydantic import (
    BaseModel,
    EmailStr,
)

from src.core.auth import Roles
from src.core.common.constants import Empty
from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.dtos import GetUserFiltersSchema


class LoginUserRequestSchema(BaseModel):
    username: str
    password: str


class GetUsersRequestSchema(BaseModel):
    """Get users requests schema."""

    filters: GetUserFiltersSchema
    pagination: PaginationSchema


class CreateUserRequestSchema(BaseModel):
    """Create users requests schema."""

    username: str
    password: str
    email: EmailStr | None = None
    phone: str | None = None


class UpdateUserRequestSchema(BaseModel):
    """Update users requests schema."""

    username: str | Empty = Empty.UNSET
    email: EmailStr | Empty = Empty.UNSET
    phone: str | Empty = Empty.UNSET


class UpdateUserRoleRequestSchema(BaseModel):
    """Update users role requests schema."""

    user_id: uuid.UUID
    role: Roles
