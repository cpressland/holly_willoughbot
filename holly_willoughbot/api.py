"""API Functions."""

from fastapi import FastAPI
from fastapi.routing import Mount
from piccolo.apps.user.tables import BaseUser
from piccolo_admin.endpoints import create_admin

from holly_willoughbot.table_config import (
    reddit_clients,
    reddit_comments,
    reddit_submissions,
    reddit_subreddits,
    telegram_clients,
)

api = FastAPI(
    routes=[
        Mount(
            path="/admin",
            app=create_admin(
                tables=[
                    BaseUser,
                    reddit_clients,
                    reddit_comments,
                    reddit_submissions,
                    reddit_subreddits,
                    telegram_clients,
                ],
                site_name="Holly Willoughbot",
            ),
        ),
    ],
)
