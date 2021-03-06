from fastapi import APIRouter

from app.api.endpoints import category, item, login, user
from app.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(login.router, tags=["Auth"])
router.include_router(user.router, prefix="/user", tags=["User"])
router.include_router(category.router, prefix="/category", tags=["Category"])
router.include_router(item.router, prefix="/item", tags=["Item"])
