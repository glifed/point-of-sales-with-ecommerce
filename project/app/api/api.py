from fastapi import APIRouter

from app.core.config import get_settings
from app.api.endpoints import (
    category,
    login,
    user,
    ping
)

settings = get_settings()

router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(ping.router, tags=["Ping"])
router.include_router(login.router, tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(category.router, prefix="/category", tags=["Category"])
