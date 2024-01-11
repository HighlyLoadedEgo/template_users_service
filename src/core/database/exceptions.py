from src.core.common import BaseAppException


class CommitErrorException(BaseAppException):
    """Exception raised when commit errors occur."""


class RollbackErrorException(BaseAppException):
    """Exception raised when rollback errors occur."""


class RepositoryException(BaseAppException):
    """Exception raised when repo errors occur."""
