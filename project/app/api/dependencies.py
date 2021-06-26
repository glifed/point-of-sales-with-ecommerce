from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from pydantic import ValidationError

from app.core import security
from app.core.config import get_settings
from app.models.schema.schemas import TokenPayload, User_Pydantic
from app.resources.strings import APIResponseMessage
from app.services.user import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")
settings = get_settings()


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=APIResponseMessage.INVALID_USERNAME_PASSWORD,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return await UserService.get_user_by_id(id=token_data.sub)


async def get_current_active_user(security_scopes: SecurityScopes,
                                  current_user: User_Pydantic = Depends(get_current_user)):
    
    if not UserService.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=APIResponseMessage.INACTIVE_USER
        )
    if security_scopes.scopes:
        
        # validate required scopes (permissions)
        validate_req_scopes = await UserService.validate_req_scopes(
            req_scopes=security_scopes.scope_str,
            user_scopes=current_user.scopes,
        )

        if not validate_req_scopes:
            
            # check user granted one time pass
            validate_otscopes = await UserService.validate_onetime_scopes(
                req_scopes=security_scopes.scope_str,
                onetime_scopes=current_user.onetime_scopes,
            )
            if not validate_otscopes:

                # raise forbidden
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=APIResponseMessage.NOT_ENOUGH_PERMISSIONS
                )
    return current_user
