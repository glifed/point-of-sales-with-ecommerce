from typing import Any, Dict

from fastapi import APIRouter, status

router = APIRouter()


@router.post(
    '/',
    name="Item:Create",
    status_code=status.HTTP_201_CREATED
)
async def create_item(item_create: Dict) -> Any:
    return item_create
