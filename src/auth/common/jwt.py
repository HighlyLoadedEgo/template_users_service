from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime

from src.auth.schemas import (
    TokenPayload,
    TokensData,
    UserPayload,
)


class JWTManager(ABC):
    """Base class for JWT managers."""

    @abstractmethod
    def encode_token(self, payload: UserPayload) -> TokensData:
        """Encode a user payload into a JWT token."""

    @abstractmethod
    def refresh_tokens(self, token: str) -> TokensData:
        """Refresh tokens using refresh token."""

    @abstractmethod
    def _generate_token(
        self, payload: dict, iat: datetime, exp: datetime, type_: str
    ) -> str:
        """Generate a JWT token."""

    @abstractmethod
    def decode_token(self, token: str) -> TokenPayload:
        """Decode a JWT token and return the decoded payload."""
