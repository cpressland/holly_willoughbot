"""Settings module for Holly Willoughbot."""

import sys
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Settings for the database."""

    path: Path = Path.cwd() / "holly_willoughbot.db"

    class Config:
        """Pydantic config."""

        env_prefix = "database_"
        env_file = ".env"


class RedditSettings(BaseSettings):
    """Settings for Reddit."""

    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = "python:holly_willoughbot:v2.0.0 (by /u/cpressland)"

    class Config:
        """Pydantic config."""

        env_prefix = "reddit_"
        env_file = ".env"


class TelegramSettings(BaseSettings):
    """Settings for Telegram."""

    token: str
    chat_id: str

    class Config:
        """Pydantic config."""

        env_prefix = "telegram_"
        env_file = ".env"


database_settings = DatabaseSettings()
reddit_settings = RedditSettings()
telegram_settings = TelegramSettings()


logger_format = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level> | <green>{extra}</green>"
logger.remove()
logger.add(sys.stdout, format=logger_format)
