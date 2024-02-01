from dataclasses import dataclass

from src.core.common import BaseAppException


@dataclass(eq=False)
class ExchangeNotFound(BaseAppException):
    """Exception raised when queue was not found."""

    exchange_name: str

    @property
    def message(self) -> str:
        return f"Exchange '{self.exchange_name}' not found!"
