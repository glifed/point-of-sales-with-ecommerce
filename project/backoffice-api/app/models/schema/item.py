from typing import List

from pydantic import BaseModel

from app.models.schema.schemas import CategoryBase, ItemBase


class ResponseItemWithCategory(BaseModel):
    item: ItemBase
    category: CategoryBase


class ResponseItemList(BaseModel):
    items: List[ResponseItemWithCategory]


class ResponseItemListPaginated(ResponseItemList):
    total: int
