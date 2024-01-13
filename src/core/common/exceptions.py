from dataclasses import dataclass


@dataclass(eq=False)
class BaseAppException(Exception):
    @property
    def message(self) -> str:
        """Method for error message."""
        return "An error occurred while processing your request."
