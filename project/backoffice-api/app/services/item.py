from app.crud.crud_item import item_crud
from app.models.schema.item import ResponseItemWithCategory
from app.models.schema.schemas import Item_Pydantic, ItemIn_Pydantic
from app.resources.exceptions import ItemNotFoundException, NameTakenException
from app.services.category import category_crud


class ItemCRUDService:
    """Item CRUD operations.
    - Create item service.
    - Read item service.
    - Update item service.
    - Delete item service.
    """

    async def create(self, category_id: str, item_create: ItemIn_Pydantic):
        category = await category_crud.filter_or_none(id=category_id)
        if not category:
            raise ItemNotFoundException
        item_obj = await item_crud.create_with_related(
            item_create, "category", category
        )
        item = await Item_Pydantic.from_tortoise_orm(item_obj)
        return ResponseItemWithCategory(item=item, category=category)


class ItemValService:
    """Item validator methods."""

    async def validate_name_taken(self, name: str) -> None:
        item = await item_crud.filter_or_none(name=name)
        if item:
            raise NameTakenException
