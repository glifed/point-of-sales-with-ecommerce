from app.models.domain.category import Category
from app.models.schema.schemas import CategoryIn_Pydantic, Category_List_Pydantic, Category_Pydantic


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
