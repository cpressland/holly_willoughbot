from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, create_engine, false
from sqlalchemy.orm import declarative_base, relationship

from holly_willoughbot.settings import settings

engine = create_engine(settings.database_dsn, echo=False)
base = declarative_base()


class DB_Posts(base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True)
    subreddit = Column(String)
    title = Column(String)
    author = Column(String)
    created = Column(DateTime)
    permalink = Column(String)
    locked = Column(Boolean)
    notification_sent = Column(Boolean, server_default=false())


class DB_Comments(base):
    __tablename__ = "comments"

    id = Column(String, primary_key=True)
    post_id = Column(String, ForeignKey("posts.id"))
    author = Column(String)
    body = Column(String)
    created = Column(DateTime)
    notification_sent = Column(Boolean, server_default=false())

    posts = relationship("DB_Posts")
