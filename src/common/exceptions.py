from abc import abstractmethod


class BaseAppException(Exception):
    @abstractmethod
    @property
    def message(self) -> str:
        """Method for error message."""
