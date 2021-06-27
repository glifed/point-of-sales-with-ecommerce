from datetime import timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import jwt
from pydantic import ValidationError

from app.core import security
from app.core.config import get_settings
from app.core.security import create_access_token, create_refresh_token
from app.models.schema.schemas import TokenPayload
from app.resources.strings import APIResponseMessage

settings = get_settings()


class TokenService:
    @staticmethod
    def create_tokens(user: Any):
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            str(user.id), expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            str(user.id), expires_delta=refresh_token_expires
        )
        return access_token, refresh_token

    @staticmethod
    def validate_token(token: str) -> TokenPayload:
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

        return token_data
