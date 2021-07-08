from typing import Any, Optional

from fastapi import APIRouter, Depends, Security, status
from tortoise.exceptions import DoesNotExist, OperationalError

from app.api.dependencies import get_valid_permissions_user
from app.models.schema.category import ResponseCategory, ResponseCategoryListPaginated
from app.models.schema.schemas import CategoryIn_Pydantic, CustomResponse, User_Pydantic
from app.models.schema.security import Action, Model
from app.resources.exceptions import (
    ErrorSavingItemException,
    InvalidIdException,
    ItemNotFoundException,
)
from app.resources.strings import APIResponseMessage
from app.services.category import CategoryService

router = APIRouter()
category_service = CategoryService()

@router.get("/", name="Category:All", response_model=ResponseCategoryListPaginated)
async def get_all(skip: Optional[int] = 0, limit: Optional[int] = 100):
    """
    Get all categories.
    """

    try:
        all_category = await category_service.get_all_categories_paginated(skip, limit)

    except DoesNotExist:
        raise ItemNotFoundException

    return all_category


@router.post(
    "/",
    name="Category:Create",
    response_model=ResponseCategory,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_create: CategoryIn_Pydantic,
    current_user: User_Pydantic = Security(
        get_valid_permissions_user,
        scopes=[f"{Model.CATEGORY}:{Action.CREATE}"],
    ),
) -> Any:
    """
    Create a new category.
    """

    await category_service.validate_name_taken(category_create.name)
    try:
        category_obj = await category_service.create_category(category_create)

    except OperationalError:
        raise ErrorSavingItemException

    return ResponseCategory(**category_obj.dict())


@router.put("/{id}", name="Category:Update", response_model=ResponseCategory)
async def update_category(
    id: str,
    category_update: CategoryIn_Pydantic,
    current_user: User_Pydantic = Depends(get_valid_permissions_user),
):
    """
    Update a category.
    """

    await category_service.validate_name_taken(category_update.name)

    try:
        updated_category = await category_service.update_category(id, category_update)

    except DoesNotExist:
        raise ItemNotFoundException
    except OperationalError:
        raise InvalidIdException

    return ResponseCategory(**updated_category.dict())


@router.get("/{id}", name="Category:Get by ID", response_model=ResponseCategory)
async def get_specific_category(id: str):
    """
    Get category by ID.
    """

    try:
        category = await category_service.get_category_by_id(id)

    except DoesNotExist:
        raise ItemNotFoundException
    except OperationalError:
        raise InvalidIdException

    return ResponseCategory(**category.dict())


@router.delete("/{id}", name="Category:Delete", response_model=CustomResponse)
async def delete_category(
    id: str,
    current_user: User_Pydantic = Depends(get_valid_permissions_user),
) -> Any:
    """
    Delete a category.
    """
    try:
        deleted = await category_service.delete_category(id)
        if not deleted:
            raise DoesNotExist

    except DoesNotExist:
        raise ItemNotFoundException
    except OperationalError:
        raise InvalidIdException

    return CustomResponse(detail=APIResponseMessage.ITEM_DELETED_SUCCESSFULLY)
