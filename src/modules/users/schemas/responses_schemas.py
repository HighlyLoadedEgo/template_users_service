from src.modules.users.schemas import (
    FullUserSchema,
    UsersWithPaginationSchema,
)


class UsersResponseSchema(UsersWithPaginationSchema):
    """Response schema for get users endpoint."""


class UserResponseSchema(FullUserSchema):
    """Response schema for full data user."""
