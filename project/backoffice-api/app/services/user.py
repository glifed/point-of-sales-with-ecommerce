from fastapi import HTTPException, status

from app.core.security import get_password_hash, verify_password
from app.models.domain.base import Status
from app.models.domain.user import User
from app.models.schema.schemas import User_Pydantic
from app.resources.exceptions import (
    InactiveUserException,
    InsufficientPermissionsException,
    ItemNotFoundException,
    InvalidUsernamePasswordException,
    NameTakenException,
)
from app.resources.strings import APIResponseMessage


class UserService:
    """
    Methods related to the user.
    """

    # CRUD
    
    async def validate_username_taken(self, username):
        user = await self.get_by_username(username)
        if user:
            raise NameTakenException

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
            raise ItemNotFoundException
        return await User_Pydantic.from_tortoise_orm(user)

    @staticmethod
    async def get_by_username(username: str):
        return await User.get_or_none(username=username)

    # USER AUTHENTICATION
    
    async def authenticate(self, username: str, password: str):
        user = await self.get_by_username(username)
        if not user:
            raise InvalidUsernamePasswordException
        if not verify_password(password, user.hashed_password):
            raise InvalidUsernamePasswordException
        return user

    @staticmethod
    def validate_is_active(user: User_Pydantic) -> None:
        if not user.status == Status.ACTIVE:
            raise InactiveUserException

    # USER AUTHORIZATION
    @staticmethod
    async def validate_req_scopes(
        req_scopes: str,
        user_scopes: dict,
    ) -> bool:

        if user_scopes:
            if req_scopes in user_scopes:
                return True
            return False
        return False

    @staticmethod
    async def validate_onetime_scopes(
        req_scopes: str,
        onetime_scopes: dict,
    ) -> bool:

        if onetime_scopes:
            if req_scopes in onetime_scopes:
                return True
            return False
        return False

    
    async def validate_scopes(
        self,
        req_scopes: str,
        user: User_Pydantic,
    ) -> None:

        scopes = await self.validate_req_scopes(req_scopes, user.scopes)
        onetime_scopes = await self.validate_onetime_scopes(
            req_scopes, user.onetime_scopes
        )

        if not scopes and not onetime_scopes:
            raise InsufficientPermissionsException
