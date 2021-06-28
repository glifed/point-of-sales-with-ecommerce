from fastapi import APIRouter

from app.api.endpoints import ping
from app.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix=settings.API_V1_STR)

router.include_router(ping.router, tags=["Ping"])