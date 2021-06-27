from typing import Any

from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import OperationalError

from app.models.schema.schemas import UserIn_Pydantic
from app.models.schema.user import ResponseUser
from app.resources.exceptions import ErrorSavingItemException
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/",
    name="User:Create",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(user_create: UserIn_Pydantic) -> Any:
    """
    Create new user.
    """
    await UserService.validate_username_taken(user_create.username)
    
    try:
        user_obj = await UserService.create_user(user_create)
        user_dict = user_obj.dict()
    except OperationalError:
        ErrorSavingItemException

    return ResponseUser(**user_dict)
