from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.models.schema.category import ResponseCategory
from app.models.schema.schemas import CategoryIn_Pydantic
from app.resources import strings
from app.services.category import CategoryService


router = APIRouter()


@router.post("/", name="category:Create", response_model=ResponseCategory,
             status_code=status.HTTP_201_CREATED)
async def create_category(
    category_create: CategoryIn_Pydantic
) -> Any:
    """ 
    Create new category.
    """
    if await CategoryService.check_categoryname_is_taken(category_create.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.NAME_TAKEN
        )
    try:
        category_obj = await CategoryService.create_category(category_create)
        cat_dict = category_obj.dict()
        return ResponseCategory(**cat_dict)

    except Exception as e:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.ERROR_IN_SAVING_ITEM
        )
