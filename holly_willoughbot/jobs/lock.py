import pendulum
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, update

from holly_willoughbot.database import DB_Posts, engine
from holly_willoughbot.reddit import reddit


class ThreadLock:
    def __init__(self) -> None:
        pass

    def lock(self) -> None:
        with Session(engine) as session:
            posts = session.execute(
                select(DB_Posts).where(DB_Posts.locked.is_(False), DB_Posts.created < pendulum.now().subtract(days=30))
            )
            for (post,) in posts:
                print(f"https://www.reddit.com{post.permalink}")
                reddit.submission(id=post.id).mod.lock()
                session.execute(update(DB_Posts).where(DB_Posts.id == post.id).values(locked=True))
                session.commit()
