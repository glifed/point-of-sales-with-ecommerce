from typing import Any, Optional

from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist, OperationalError

from app.models.schema.category import (ResponseCategory,
                                        ResponseCategoryListPaginated)
from app.models.schema.schemas import CategoryIn_Pydantic, CustomResponse
from app.resources import strings
from app.services.category import CategoryService

router = APIRouter()


@router.get("/", name="Category:All", response_model=ResponseCategoryListPaginated)
async def get_all(skip: Optional[int] = 0, limit: Optional[int] = 100):
    try:
        all_category = await CategoryService.get_all_categories_paginated(skip, limit)
        return all_category
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )


@router.post(
    "/",
    name="category:Create",
    response_model=ResponseCategory,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(category_create: CategoryIn_Pydantic) -> Any:
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
        return ResponseCategory(**cat_dict)

    except Exception:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.ERROR_IN_SAVING_ITEM
        )


@router.put("/{id}", name="Category:Update Category", response_model=ResponseCategory)
async def update_category(id: str, category_update: CategoryIn_Pydantic):
    if await CategoryService.check_categoryname_is_taken(category_update.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.NAME_TAKEN
        )
    try:
        updated_category = await CategoryService.update_category(id, category_update)
        return ResponseCategory(**updated_category.dict())
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_UUID
        )


@router.get(
    "/{id}", name="Category:Get Category by ID", response_model=ResponseCategory
)
async def get_specific_category(id: str):
    try:
        category = await CategoryService.get_category_by_id(id)
        return ResponseCategory(**category.dict())
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_UUID
        )


@router.delete("/{id}", response_model=CustomResponse)
async def delete_category(id: str):
    try:
        deleted = await CategoryService.delete_category(id)
        if not deleted:
            raise DoesNotExist
        return CustomResponse(detail=strings.ITEM_DELETED_SUCCESSFULLY)

    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=strings.ITEM_NOT_FOUND_IN_DB
        )
    except OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=strings.INVALID_UUID
        )
