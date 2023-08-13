"""Module containing logic for locking Reddit Threads."""
import pendulum
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, update

from holly_willoughbot.database import DBPosts, engine
from holly_willoughbot.reddit import reddit


class ThreadLock:
    """Class for locking Redit Threads."""

    def __init__(self) -> None:
        """Initialize the ThreadLock class."""

    def lock(self) -> None:
        """Lock Thread if older than 30 days."""
        logger.warning("Beginning Thread Locking")
        with Session(engine) as session:
            posts = session.execute(
                select(DBPosts).where(DBPosts.locked.is_(False), DBPosts.created < pendulum.now().subtract(days=30)),
            )
            for (post,) in posts:
                logger.warning(f"Locking: {post.id}")
                reddit.submission(id=post.id).mod.lock()
                session.execute(update(DBPosts).where(DBPosts.id == post.id).values(locked=True))
                session.commit()
