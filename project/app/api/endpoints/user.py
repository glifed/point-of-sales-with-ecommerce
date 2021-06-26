from typing import Any

from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import OperationalError

from app.models.schema.user import (ResponseUser,
                                    ResponseUserList,
                                    ResponseUserListPaginated)
from app.models.schema.schemas import UserIn_Pydantic
from app.resources.strings import APIResponseMessage
from app.services.user import UserService

router = APIRouter()


@router.post(
    "/",
    name="User:Create",
    response_model=ResponseUser,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_create: UserIn_Pydantic
) -> Any:
    """
    Create new user.
    """
    if await UserService.check_username_is_taken(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=APIResponseMessage.NAME_TAKEN
        )
    try:
        user_obj = await UserService.create_user(user_create)
        user_dict = user_obj.dict()
    except OperationalError:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=APIResponseMessage.ERROR_IN_SAVING_ITEM
        )
    
    return ResponseUser(**user_dict)
