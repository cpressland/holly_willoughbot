"""Project Settings."""

from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings

if TYPE_CHECKING:
    from pydantic import PostgresDsn


class Settings(BaseSettings):
    """Settings for the bot."""

    database_url: PostgresDsn = "postgres://postgres:password@localhost/holly_willoughbot"


settings = Settings()
