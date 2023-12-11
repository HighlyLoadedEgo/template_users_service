from abc import abstractmethod


class BaseAppException(Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        """Method for error message."""
