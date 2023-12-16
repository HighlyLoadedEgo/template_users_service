import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
)

from src.auth.constants import Roles


class UserPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    role: Roles


class TokenPayload(UserPayload):
    type: str
    exp: datetime.datetime
    iat: datetime.datetime
    fingerprint: str | None = None


class TokensData(BaseModel):
    access_token: str
    refresh_token: str
