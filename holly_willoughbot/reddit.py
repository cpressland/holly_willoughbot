"""Setup the praw library."""
import praw

from holly_willoughbot.settings import settings

reddit = praw.Reddit(
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    user_agent=settings.user_agent,
    username=settings.reddit_username,
    password=settings.reddit_password,
)
