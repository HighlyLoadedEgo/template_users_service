from pydantic import BaseModel

from src.common.constants import Empty
from src.database import SortOrder


class PaginationSchema(BaseModel):
    offset: int | Empty = Empty.UNSET
    limit: int | Empty = Empty.UNSET
    order: SortOrder = SortOrder.ASC
