from typing import Any

from fastapi import APIRouter, status
from tortoise.exceptions import DoesNotExist, OperationalError

from app.models.schema.schemas import ItemIn_Pydantic
from app.models.schema.item import ResponseItemWithCategory
from app.resources.exceptions import ErrorSavingItemException
from app.services.item import ItemCRUDService, ItemValService

router = APIRouter()
item_crud_service = ItemCRUDService()
item_validators = ItemValService()


@router.post("/{category_id}", name="Item:Create", status_code=status.HTTP_201_CREATED)
async def create_item(category_id: str, item_create: ItemIn_Pydantic) -> Any:
    """Create an item"""
    await item_validators.validate_name_taken(item_create.name)
    try:
        item_obj = await item_crud_service.create(category_id, item_create)
    except OperationalError:
        raise ErrorSavingItemException
    return ResponseItemWithCategory(**item_obj.dict())
