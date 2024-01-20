import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)

from src.core.auth import Roles
from src.core.common.constants import Empty
from src.core.database.postgres.schemas import PaginationSchema


class FullUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: EmailStr | None = None
    phone: str | None = None
    role: Roles
    is_deleted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    hashed_password: str


class LoginUserSchema(BaseModel):
    username: str
    password: str


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    email: EmailStr | None = None
    phone: str | None = None


class UpdateUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    username: str | Empty = Empty.UNSET
    email: EmailStr | Empty = Empty.UNSET
    phone: str | Empty = Empty.UNSET
    role: Roles | Empty = Empty.UNSET


class UsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[FullUserSchema]


class GetUserFiltersSchema(BaseModel):
    deleted: bool | Empty = Empty.UNSET
    role: Roles | Empty = Empty.UNSET
    username: str | Empty = Empty.UNSET


class UsersWithPaginationSchema(PaginationSchema):
    users: list[FullUserSchema] | None
    total: int | None
