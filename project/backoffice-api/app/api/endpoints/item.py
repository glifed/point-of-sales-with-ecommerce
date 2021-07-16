from typing import Any

from fastapi import APIRouter, status
from tortoise.exceptions import OperationalError

from app.models.schema.schemas import ItemIn_Pydantic
from app.resources.exceptions import ErrorSavingItemException
from app.services.item import ItemCRUDService, ItemValService

router = APIRouter()
item_crud_service = ItemCRUDService()
item_validators = ItemValService()


@router.post("/{category_id}", name="Item:Create", status_code=status.HTTP_201_CREATED)
async def create_item(category_id: str, item_create: ItemIn_Pydantic) -> Any:
    """Create an item. Category is a mandatory field,
    no item should be created without category.
    """
    await item_validators.validate_name_taken(item_create.name)
    try:
        item_with_category = await item_crud_service.create(category_id, item_create)
    except OperationalError:
        raise ErrorSavingItemException
    return item_with_category
