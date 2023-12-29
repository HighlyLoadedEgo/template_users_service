from dataclasses import dataclass

from src.core.auth.constants import Roles
from src.core.common.exceptions import BaseAppException


@dataclass(eq=False)
class AccessDeniedException(BaseAppException):
    """Exception raised when an access denied."""

    role: str = Roles.USER.value

    @property
    def message(self) -> str:
        return f"Access for role {self.role} denied!"


class InvalidTokenException(BaseAppException):
    """Exception raised when an invalid token is provided."""

    @property
    def message(self) -> str:
        return "Invalid token data."
