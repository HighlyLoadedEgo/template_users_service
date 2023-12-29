from pydantic import BaseModel

from src.core.database.postgres.schemas import PaginationSchema
from src.modules.users.schemas import GetUserFiltersSchema


class GetUsersRequestSchema(BaseModel):
    """Get users requests schema."""

    filters: GetUserFiltersSchema
    pagination: PaginationSchema
