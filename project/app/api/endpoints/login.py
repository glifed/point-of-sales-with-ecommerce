from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token
from app.models.schema.schemas import TokenResponse
from app.resources.strings import APIResponseMessage
from app.services.user import UserService

settings = get_settings()

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await UserService.authenticate(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=APIResponseMessage.INVALID_USERNAME_PASSWORD
        )
    if not UserService.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=APIResponseMessage.INACTIVE_USER
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(str(user.id),
                                       expires_delta=access_token_expires)
    refresh_token = create_refresh_token(str(user.id),
                                         expires_delta=refresh_token_expires)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
