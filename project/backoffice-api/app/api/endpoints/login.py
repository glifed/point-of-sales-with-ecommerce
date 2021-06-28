from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.models.schema.schemas import TokenResponse
from app.services.security import TokenService
from app.services.user import UserService

settings = get_settings()

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible login, get tokens for future requests.
    """

    user = await UserService.authenticate(form_data.username, form_data.password)
    UserService.validate_is_active(user)
    access_token, refresh_token = TokenService.create_tokens(user)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)
