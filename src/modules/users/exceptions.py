from dataclasses import dataclass

from src.common.exceptions import BaseAppException


@dataclass(eq=True)
class UserIsExistException(BaseAppException):
    """Base exception for user"""

    invalid_data: list[str] | str = "data"

    @property
    def message(self) -> str:
        return f"User with this {self.invalid_data} is already registered!"


@dataclass(eq=True)
class UserDoesNotExistException(UserIsExistException):
    """Exception raised when user does not exist."""

    data: str = "data"

    @property
    def message(self) -> str:
        return f"User with this {self.data} is not registered!"


class IncorrectUserCredentialsException(UserIsExistException):
    """Exception raised when incorrect credentials was sent by user."""

    @property
    def message(self) -> str:
        return "Incorrect credentials!"
