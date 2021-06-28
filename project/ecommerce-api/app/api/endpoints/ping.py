from fastapi import APIRouter, Depends

from app.core.config import get_settings, Settings

router = APIRouter()

settings = get_settings()

@router.get("/ping")
async def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }