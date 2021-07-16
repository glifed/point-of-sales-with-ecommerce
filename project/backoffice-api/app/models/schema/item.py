from typing import List

from pydantic import BaseModel

from app.models.schema.schemas import CategoryBase
from app.models.schema.schemas import ItemBase


class ResponseItemWithCategory(ItemBase):
    category: CategoryBase


class ResponseItemList(BaseModel):
    items: List[ResponseItemWithCategory]


class ResponseItemListPaginated(ResponseItemList):
    total: int
