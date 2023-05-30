from pydantic import BaseSettings


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    user_agent: str = "python:holly_willoughbot:v1.0.0 (by /u/cpressland)"
    reddit_username: str = "holly_willoughbot"
    reddit_password: str
    telegram_token: str
    database_dsn: str = "postgresql+psycopg://postgres@localhost:5432/postgres"
    notifications_enabled: bool = True
    subreddits: str = "TheHollyWilloughby"
    subreddit_search_limit: int = 25


settings = Settings()
