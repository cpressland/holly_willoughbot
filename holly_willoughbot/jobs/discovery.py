from time import sleep

import pendulum
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import Session

from holly_willoughbot.database import DB_Comments, DB_Posts, engine
from holly_willoughbot.reddit import reddit
from holly_willoughbot.settings import settings


class Discovery:
    def __init__(self) -> None:
        pass

    def posts(self) -> None:
        with Session(engine) as session:
            for subreddit in settings.subreddits.split(","):
                logger.warning(f"Processing Subreddit: {subreddit}")
                for post in reddit.subreddit(subreddit).new(limit=settings.subreddit_search_limit):
                    logger.info(f"Processing post: {post.id}, Archived: {post.archived}")
                    try:
                        insert = DB_Posts(
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
        with Session(engine) as session:
            for subreddit in settings.subreddits.split(","):
                logger.warning(f"Processing Subreddit: {subreddit}")
                posts = session.execute(
                    select(DB_Posts.id).where(DB_Posts.subreddit == subreddit).where(DB_Posts.locked.is_(False))
                ).all()
                for (post_id,) in posts:
                    for comment in reddit.submission(id=post_id).comments.list():
                        try:
                            insert = DB_Comments(
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

    def loop(self) -> None:
        while True:
            self.posts()
            self.comments()
            logger.warning("Discovery Complete, sleeping for 5 minutes")
            sleep(300)
