import logging
from functools import lru_cache
from typing import List

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings

load_dotenv()
log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """
    Contains app default settings.
    """

    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str
    TESTING: bool
    DATABASE_URL: AnyUrl
    DATABASE_TEST_URL: AnyUrl
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
