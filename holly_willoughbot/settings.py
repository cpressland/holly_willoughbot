"""Project Settings."""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the bot."""

    database_url: PostgresDsn = "postgres://postgres:password@localhost/holly_willoughbot"


settings = Settings()
