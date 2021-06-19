from fastapi import APIRouter, Depends

from config.settings import get_settings, Settings

router = APIRouter()


@router.get("/ping")
async def pong(settings: Settings=Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.ENVIRONMENT,
        "testing": settings.TESTING,
    }
