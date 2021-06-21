from fastapi import APIRouter

from app.api.endpoints import category, ping

router = APIRouter()

router.include_router(ping.router, tags=["testing"])
router.include_router(category.router, prefix="/category", tags=["Category"])
