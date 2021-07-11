from typing import List

from app.crud.base import CRUDBase
from app.models.domain.category import Category
from app.models.schema.category import ResponseCategoryListPaginated
from app.models.schema.schemas import (
    Category_List_Pydantic,
    Category_Pydantic,
    CategoryIn_Pydantic,
)


class CRUDCategory(CRUDBase):
    pass


category_crud = CRUDCategory(Category)
