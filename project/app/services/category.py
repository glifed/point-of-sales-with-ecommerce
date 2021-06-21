from app.models.domain.category import Category
from app.models.schema.category import ResponseCategoryListPaginated
from app.models.schema.schemas import (
    Category_List_Pydantic,
    Category_Pydantic,
    CategoryIn_Pydantic,
)


class CategoryService:
    @staticmethod
    async def create_category(category_create):
        category = Category(**category_create.dict())
        await category.save()
        return await Category_Pydantic.from_tortoise_orm(category)

    @staticmethod
    async def check_categoryname_is_taken(name: str):
        category = await Category.get_or_none(name=name)
        if category:
            return True
        return False

    @staticmethod
    async def get_all_categories():
        category = await Category_List_Pydantic.from_queryset(Category.all())
        return category

    @staticmethod
    async def get_all_categories_paginated(skip: int = 0, limit: int = 100):
        category = await Category_List_Pydantic.from_queryset(
            Category.all().offset(skip).limit(limit)
        )
        count = await Category.all().count()
        return ResponseCategoryListPaginated(
            categories=category.dict()["__root__"], total=count
        )

    @staticmethod
    async def get_category_by_id(id: str):
        category = await Category.get(id=id)
        return await Category_Pydantic.from_tortoise_orm(category)

    @classmethod
    async def update_category(cls, id: str, category: CategoryIn_Pydantic):
        await Category.filter(id=id).update(**category.dict(exclude_unset=True))
        return await cls.get_category_by_id(id)

    @staticmethod
    async def delete_category(id: str):
        deleted_count = await Category.filter(id=id).delete()
        if not deleted_count:
            return False
        return True
