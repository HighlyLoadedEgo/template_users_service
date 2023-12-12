from pydantic import (
    BaseModel,
    Field,
)

from src.auth.constants import (
    PRIVATE_KEY_PATH,
    PUBLIC_KEY_PATH,
)
from src.auth.utils import key_loader


class JWTConfig(BaseModel):
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    public_key: str = Field(
        description="Public key", default=key_loader(PUBLIC_KEY_PATH)
    )
    private_key: str = Field(
        description="The private key", default=key_loader(PRIVATE_KEY_PATH)
    )
