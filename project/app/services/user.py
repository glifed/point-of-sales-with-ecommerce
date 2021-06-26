from typing import List

from fastapi import HTTPException, status

from app.core.security import get_password_hash, verify_password
from app.models.domain.base import Status
from app.models.domain.user import User
from app.models.schema.schemas import User_Pydantic
from app.resources.strings import APIResponseMessage


class UserService:
    """
    Methods related to the user.
    """

    @classmethod
    async def check_username_is_taken(cls, username):
        user = await cls.get_by_username(username)
        if user:
            return True
        return False

    
    # CRUD
    @staticmethod
    async def create_user(user_create):
        # hash password
        user_create.hashed_password = get_password_hash(user_create.hashed_password)
        
        # add to db
        user = User(**user_create.dict(exclude_unset=True))
        await user.save()
        return await User_Pydantic.from_tortoise_orm(user)

    
    @staticmethod
    async def get_user_by_id(id: str):
        user = await User.get_or_none(id=id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=APIResponseMessage.ITEM_NOT_FOUND,
            )
        return await User_Pydantic.from_tortoise_orm(user)

    
    # User Authentication
    @staticmethod
    async def get_by_username(username: str):
        return await User.get_or_none(username=username)
    

    @classmethod    
    async def authenticate(cls, username: str, password: str):
        user = await cls.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    

    @staticmethod
    def is_active(user: User_Pydantic):
        return user.status == Status.ACTIVE
    
    
    # User Authorization
    @staticmethod
    async def validate_req_scopes(
        req_scopes: str, user_scopes: dict,
    ) -> bool:
        
        if user_scopes:
            if req_scopes in user_scopes:
                return True
            return False
        return False
    

    @staticmethod
    async def validate_onetime_scopes(
        req_scopes: str, onetime_scopes: dict,
    ) -> bool:
        
        if onetime_scopes:
            if req_scopes in onetime_scopes:
                return True
            return False
        return False
