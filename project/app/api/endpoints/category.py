from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist, OperationalError

from app.api.dependencies import get_current_active_user
from app.models.schema.category import (ResponseCategory,
                                        ResponseCategoryListPaginated)
from app.models.schema.schemas import CategoryIn_Pydantic, CustomResponse, User_Pydantic
from app.resources import strings
from app.services.category import CategoryService

router = APIRouter()


@router.get("/", name="Category:All", response_model=ResponseCategoryListPaginated)
async def get_all(skip: Optional[int] = 0, limit: Optional[int] = 100):
    try:
        all_category = await CategoryService.get_all_categories_paginated(skip, limit)
    
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    
    return all_category


@router.post(
    "/",
    name="Category:Create",
    response_model=ResponseCategory,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category_create: CategoryIn_Pydantic,
    current_user: User_Pydantic = Depends(get_current_active_user)
) -> Any:
    """
    Create new category.
    """
    if await CategoryService.check_categoryname_is_taken(category_create.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.NAME_TAKEN
        )
    try:
        category_obj = await CategoryService.create_category(category_create)
        cat_dict = category_obj.dict()

    except OperationalError:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.ERROR_IN_SAVING_ITEM
        )
    
    return ResponseCategory(**cat_dict)


@router.put("/{id}", name="Category:Update Category", response_model=ResponseCategory)
async def update_category(
    id: str,
    category_update: CategoryIn_Pydantic,
    current_user: User_Pydantic = Depends(get_current_active_user),
):
    if await CategoryService.check_categoryname_is_taken(category_update.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.NAME_TAKEN
        )
    try:
        updated_category = await CategoryService.update_category(id, category_update)
    
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_UUID
        )
    
    return ResponseCategory(**updated_category.dict())


@router.get(
    "/{id}", name="Category:Get Category by ID", response_model=ResponseCategory
)
async def get_specific_category(id: str):
    try:
        category = await CategoryService.get_category_by_id(id)
    
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_UUID
        )
    
    return ResponseCategory(**category.dict())


@router.delete("/{id}", response_model=CustomResponse)
async def delete_category(
    id: str,
    current_user: User_Pydantic = Depends(get_current_active_user),
):
    try:
        deleted = await CategoryService.delete_category(id)
        if not deleted:
            raise DoesNotExist

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_UUID
        )
    
    return CustomResponse(detail=strings.ITEM_DELETED_SUCCESSFULLY)
