from app.crud.crud_category import category_crud
from app.models.schema.category import ResponseCategoryListPaginated
from app.models.schema.schemas import (
    Category_List_Pydantic,
    Category_Pydantic,
    CategoryIn_Pydantic,
)
from app.resources.exceptions import NameTakenException


class CategoryCRUDService:
    """Category CRUD operations.
    - Create category service.
    - Read category service.
    - Update category service.
    - Delete category service.
    """

    async def create_category(self, category_create: CategoryIn_Pydantic):
        category = await category_crud.create(category_create)
        return await Category_Pydantic.from_tortoise_orm(category)

    async def get_all_categories_paginated(self, skip: int = 0, limit: int = 100):
        categories_obj = await Category_List_Pydantic.from_queryset(
            category_crud.get_all(skip=skip, limit=limit)
        )

        count = await category_crud.get_count()
        return ResponseCategoryListPaginated(
            categories=categories_obj.dict()["__root__"], total=count
        )

    async def get_category_by_id(self, id: str):
        category = await category_crud.filter_by_query(id=id)
        return await Category_Pydantic.from_tortoise_orm(category)

    async def update_category(self, id: str, category_update: CategoryIn_Pydantic):
        await category_crud.update(id, category_update)
        return await self.get_category_by_id(id)

    async def delete_category(self, id: str):
        deleted_count = await category_crud.delete(id)
        if not deleted_count:
            return False
        return True


class CategoryValService:
    """Category validators"""

    async def validate_name_taken(self, name: str) -> None:
        category = await category_crud.filter_or_none(name=name)
        if category:
            raise NameTakenException
