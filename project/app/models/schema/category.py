from typing import List

from pydantic import BaseModel

from app.models.schema.schemas import CategoryInfo


class ResponseCategory(CategoryInfo):
    pass


class ResponseCategoryList(BaseModel):
    categories: List[CategoryInfo]
