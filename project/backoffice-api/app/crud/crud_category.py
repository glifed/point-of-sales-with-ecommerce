from app.crud.base import CRUDBase
from app.models.domain.category import Category


class CRUDCategory(CRUDBase):
    pass


category_crud = CRUDCategory(Category)
