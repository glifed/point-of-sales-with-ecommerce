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


class UserCRUDService:
    """User CRUD operations.
    - Create user service.
    - Read user service.
    - Update user service.
    - Delete user service.
    """

    async def get_by_username(self, username: str):
        return await User.get_or_none(username=username)

    async def validate_username_taken(self, username):
        user = await self.get_by_username(username)
        if user:
            raise NameTakenException

    async def create_user(self, user_create):
        user_create.hashed_password = get_password_hash(user_create.hashed_password)
        user = User(**user_create.dict(exclude_unset=True))
        await user.save()
        return await User_Pydantic.from_tortoise_orm(user)

    async def get_user_by_id(self, id: str):
        user = await User.get_or_none(id=id)
        if not user:
            raise ItemNotFoundException
        return await User_Pydantic.from_tortoise_orm(user)


class UserAuthService:
    """User Authentition and Authorization validators."""

    async def authenticate(self, username: str, password: str):
        user = await UserCRUDService().get_by_username(username)
        if not user:
            raise InvalidUsernamePasswordException
        if not verify_password(password, user.hashed_password):
            raise InvalidUsernamePasswordException
        return user

    def validate_is_active(self, user: User_Pydantic) -> None:
        if not user.status == Status.ACTIVE:
            raise InactiveUserException

    async def validate_req_scopes(
        self,
        req_scopes: str,
        user_scopes: dict,
    ) -> bool:

        if user_scopes:
            if req_scopes in user_scopes:
                return True
            return False
        return False

    async def validate_onetime_scopes(
        self,
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
