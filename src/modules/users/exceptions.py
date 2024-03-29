from dataclasses import dataclass
from uuid import UUID

from src.core.common import BaseAppException


@dataclass(eq=True)
class UserDataIsExistException(BaseAppException):
    """Base exception for user"""

    attribute: str = "data"

    @property
    def message(self) -> str:
        return f"User with '{self.attribute}' is already registered!"


@dataclass(eq=True)
class UserDoesNotExistException(BaseAppException):
    """Exception raised when user does not exist."""

    search_data: str | UUID

    @property
    def message(self) -> str:
        return f"User with this data -> {self.search_data} is not registered!"


class IncorrectUserCredentialsException(BaseAppException):
    """Exception raised when incorrect credentials was sent by user."""

    @property
    def message(self) -> str:
        return "Incorrect credentials!"
