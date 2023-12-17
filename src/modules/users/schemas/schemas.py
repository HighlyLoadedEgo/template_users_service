import datetime
import uuid

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    model_validator,
)

from src.auth import Roles
from src.common.constants import Empty
from src.database import SortOrder
from src.modules.users.utils import generate_password_hash


class FullUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: EmailStr | None = None
    phone: str | None = None
    role: str
    is_deleted: bool
    inserted_at: datetime.datetime
    updated_at: datetime.datetime
    hashed_password: bytes


class LoginUserSchema(BaseModel):
    username: str
    password: str


class CreateUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str
    email: EmailStr | None = None
    phone: str | None = None

    @model_validator(mode="before")
    def serialize(cls, values: dict) -> dict:
        values["hashed_password"] = generate_password_hash(password=values["password"])
        return values


class UpdateUserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    username: str | Empty = Empty.UNSET
    email: EmailStr | Empty = Empty.UNSET
    phone: str | Empty = Empty.UNSET
    password: str | Empty = Empty.UNSET
    role: Roles | Empty = Empty.UNSET


class UsersSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[FullUserSchema]


class GetUserFiltersSchema(BaseModel):
    deleted: bool | Empty = Empty.UNSET
    roles: list[Roles] | Empty = Empty.UNSET


class UsersWithPaginationSchema(BaseModel):
    users: list[FullUserSchema] | None
    total: int
    limit: int
    offset: int
    sort_by: SortOrder
