class DatabaseException(Exception):
    """Base class for exceptions in this module."""


class CommitErrorException(DatabaseException):
    """Exception raised when commit errors occur."""


class RollbackErrorException(DatabaseException):
    """Exception raised when rollback errors occur."""
