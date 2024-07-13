import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    SQLALCHEMY_DATABASE_URL: str
    ALGORITHM: str

    class Config:
        env_file = ".env.development"  # Default to the development environment


@lru_cache(maxsize=None)
def get_settings() -> Settings:
    # Determine the environment
    environment = os.getenv("ENVIRONMENT", "development")

    if environment == "production":
        load_dotenv(".env.production")
    elif environment == "development":
        load_dotenv(".env.development")
    else:
        raise ValueError("Unknown environment")

    return Settings()
