from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.models.schema.schemas import TokenResponse
from app.services.security import TokenService
from app.services.user import UserAuthService

settings = get_settings()

user_auth_service = UserAuthService()

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible login, get tokens for future requests.
    """

    user = await user_auth_service.authenticate(form_data.username, form_data.password)
    user_auth_service.validate_is_active(user)
    access_token, refresh_token = TokenService.create_tokens(user)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
