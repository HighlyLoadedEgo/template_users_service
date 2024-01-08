from pydantic import (
    BaseModel,
    EmailStr,
)

from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.schemas import GetUserFiltersSchema


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
