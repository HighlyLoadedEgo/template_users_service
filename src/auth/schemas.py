import datetime

from pydantic import BaseModel

from src.auth.constants import Roles


class UserPayload(BaseModel):
    user_id: int
    role: Roles


class TokenPayload(UserPayload):
    type: str
    exp: datetime.datetime
    iat: datetime.datetime
    fingerprint: str | None = None


class TokensData(BaseModel):
    access_token: str
    refresh_token: str
