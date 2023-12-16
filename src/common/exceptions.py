from abc import abstractmethod
from dataclasses import dataclass


@dataclass(eq=False)
class BaseAppException(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        """Method for error message."""
