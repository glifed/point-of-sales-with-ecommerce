from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.models.schema.schemas import User_Pydantic
from app.services.security import TokenService
from app.services.user import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
user_service = UserService()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User_Pydantic:
    """
    Validate JWT token and return current user.
    """

    token_data = TokenService.validate_token(token)

    return await user_service.get_user_by_id(id=token_data.sub)


async def get_current_active_user(
    current_user: User_Pydantic = Depends(get_current_user),
) -> User_Pydantic:
    """
    Validate current user is active.
    """

    user_service.validate_is_active(current_user)

    return current_user


async def get_valid_permissions_user(
    security_scopes: SecurityScopes,
    current_user: User_Pydantic = Depends(get_current_active_user),
) -> User_Pydantic:
    """
    Validate Current user has required scopes (Permissions).
    """

    if not current_user.is_superuser:
        if security_scopes.scopes:
            await user_service.validate_scopes(
                req_scopes=security_scopes.scope_str,
                user=current_user,
            )

    return current_user
