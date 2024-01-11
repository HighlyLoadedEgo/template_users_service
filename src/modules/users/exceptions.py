from dataclasses import dataclass

from src.core.common import BaseAppException


@dataclass(eq=True)
class UserDataIsExistException(BaseAppException):
    """Base exception for user"""

    data: list[str] | str = "data"

    @property
    def message(self) -> str:
        return f"User with data '{self.data}' is already registered!"


@dataclass(eq=True)
class UserDoesNotExistException(BaseAppException):
    """Exception raised when user does not exist."""

    data: str = "data"

    @property
    def message(self) -> str:
        return f"User with this {self.data} is not registered!"


class IncorrectUserCredentialsException(BaseAppException):
    """Exception raised when incorrect credentials was sent by user."""

    @property
    def message(self) -> str:
        return "Incorrect credentials!"
