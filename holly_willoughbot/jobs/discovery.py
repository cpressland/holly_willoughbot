"""Module containing Thread Discovery Features."""
import pendulum
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from holly_willoughbot.database import DBComments, DBPosts, engine
from holly_willoughbot.reddit import reddit
from holly_willoughbot.settings import settings


class Discovery:
    """Class for discovering new content."""

    def __init__(self) -> None:
        """Initialize the Discovery Class."""

    def posts(self) -> None:
        """Scan each subreddit defined in settings.subreddits for new posts and create a record in the database."""
        logger.warning("Beginning Post Discovery")
        with Session(engine) as session:
            for subreddit in settings.subreddits.split(","):
                logger.warning(f"Processing Subreddit: {subreddit}")
                for post in reddit.subreddit(subreddit).new(limit=settings.subreddit_search_limit):
                    logger.info(f"Processing post: {post.id}")
                    try:
                        insert = DBPosts(
                            id=post.id,
                            subreddit=subreddit,
                            title=post.title,
                            author=post.author.name,
                            permalink=post.permalink,
                            created=pendulum.from_timestamp(post.created_utc),
                            locked=post.locked if not post.archived else post.archived,
                        )
                    except AttributeError:
                        continue
                    session.merge(insert)
                session.commit()

    def comments(self) -> None:
        """Scan every unlocked post in the database for new comments."""
        logger.warning("Beginning Comment Discovery")
        with Session(engine) as session:
            for subreddit in settings.subreddits.split(","):
                logger.warning(f"Processing Subreddit: {subreddit}")
                posts = session.execute(
                    select(DBPosts.id).where(DBPosts.subreddit == subreddit).where(DBPosts.locked.is_(False)),
                ).all()
                for (post_id,) in posts:
                    for comment in reddit.submission(id=post_id).comments.list():
                        logger.info(f"Processing Comment: {comment.id}")
                        try:
                            insert = DBComments(
                                id=comment.id,
                                post_id=post_id,
                                body=comment.body,
                                author=comment.author.name,
                                permalink=comment.permalink,
                                created=pendulum.from_timestamp(comment.created_utc),
                            )
                        except AttributeError:
                            continue
                        session.merge(insert)
                    session.commit()
