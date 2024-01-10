import datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    field_serializer,
)

from src.core.auth.constants import Roles


class UserPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    role: Roles

    @field_serializer("id")
    @classmethod
    def id_serializer(cls, id_: UUID) -> str:
        return str(id_)


class TokenPayload(UserPayload):
    type: str
    exp: datetime.datetime
    iat: datetime.datetime
    fingerprint: str | None = None


class TokensData(BaseModel):
    access_token: str
    refresh_token: str
