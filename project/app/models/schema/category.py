from typing import List

from pydantic import BaseModel

from app.models.schema.schemas import CategoryBase


class ResponseCategory(CategoryBase):
    pass


class ResponseCategoryList(BaseModel):
    categories: List[CategoryBase]


class ResponseCategoryListPaginated(ResponseCategoryList):
    total: int
