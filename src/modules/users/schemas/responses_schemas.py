import datetime
import uuid

from pydantic import (
    BaseModel,
    EmailStr,
)

from src.core.common.constants import Empty
from src.core.database.postgres.constants import SortOrder


class FullUserResponseSchema(BaseModel):
    """Response schema for full data user."""

    id: uuid.UUID
    username: str
    email: EmailStr | None = None
    phone: str | None = None
    role: str
    is_deleted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UsersResponseSchema(BaseModel):
    """Response schema for get users endpoint."""

    users: list[FullUserResponseSchema] | None
    total: int | None
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    order: SortOrder = SortOrder.ASC


class TokensDataResponse(BaseModel):
    """Response schema for tokens endpoint."""

    access_token: str
    refresh_token: str
