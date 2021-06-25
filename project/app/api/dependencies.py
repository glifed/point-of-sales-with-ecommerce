from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.core import security
from app.core.config import get_settings
from app.models.schema.schemas import TokenPayload, User_Pydantic
from app.resources import strings
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
            detail=strings.INVALID_USERNAME_PASSWORD,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return await UserService.get_user_by_id(id=token_data.sub)


def get_current_active_user(current_user: User_Pydantic = Depends(get_current_user)):
    if not UserService.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=strings.INACTIVE_USER
        )
    return current_user
