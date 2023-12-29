from pydantic import BaseModel

from src.core.common.constants import Empty
from src.core.database.postgres.constants import SortOrder


class PaginationSchema(BaseModel):
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    order: SortOrder = SortOrder.ASC
