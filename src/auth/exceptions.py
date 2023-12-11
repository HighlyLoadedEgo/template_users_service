from src.common.exceptions import BaseAppException


class AccessDeniedException(BaseAppException):
    """Exception raised when an access denied."""

    @property
    def message(self) -> str:
        return "Access for this role denied!"


class InvalidTokenException(BaseAppException):
    """Exception raised when an invalid token is provided."""

    @property
    def message(self) -> str:
        return "Invalid token data."
