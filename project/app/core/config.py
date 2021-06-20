import logging
from functools import lru_cache
from typing import List, Union

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyUrl, AnyHttpUrl, validator


load_dotenv()
log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """
    Contains app default settings.
    """
    ENVIRONMENT: str
    TESTING: bool
    DATABASE_URL: AnyUrl
    DATABASE_TEST_URL: AnyUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]
    MODELS: List[str] = [
        "app.models.domain.category"
    ]
    MODELS_IN: List[str] = [  # when running within namespace
        "models.domain.category"
    ]


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
