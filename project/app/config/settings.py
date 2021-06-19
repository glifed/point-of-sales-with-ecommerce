import logging
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, AnyUrl

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

@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
