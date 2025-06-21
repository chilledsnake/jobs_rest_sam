import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_ENV: str = "local"
    APP_AWS_REGION_NAME: Optional[str] = ""
    APP_AWS_COGNITO_APP_CLIENT_ID: Optional[str] = ""
    APP_AWS_COGNITO_USER_POOL_ID: Optional[str] = ""

    if os.getenv("APP_ENV", "local") == "local":
        model_config = SettingsConfigDict(env_file=".env")


settings = Settings()


@lru_cache
def get_settings():
    return settings


env_vars = get_settings()
