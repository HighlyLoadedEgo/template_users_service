from dataclasses import dataclass
from typing import Any


@dataclass(eq=False)
class BaseAppException(Exception):
    data: Any = None

    @property
    def message(self) -> str:
        """Method for error message."""
        return "An error occurred while processing your request."
