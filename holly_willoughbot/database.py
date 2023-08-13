"""Module containing Database Schema Classes."""
from datetime import datetime

from sqlalchemy import ForeignKey, create_engine, false
from sqlalchemy.orm import DeclarativeBase, Mapped, declarative_base, mapped_column, relationship

from holly_willoughbot.settings import settings

engine = create_engine(settings.database_dsn, echo=False)
Base: DeclarativeBase = declarative_base()


class DBPosts(Base):
    """Database Table containing a record of all discovered Posts."""

    __tablename__ = "posts"

    id: Mapped[str] = mapped_column(primary_key=True)  # noqa: A003
    subreddit: Mapped[str | None]
    title: Mapped[str | None]
    author: Mapped[str | None]
    created: Mapped[datetime | None]
    permalink: Mapped[str | None]
    locked: Mapped[bool | None]
    notification_sent: Mapped[bool] = mapped_column(server_default=false())


class DBComments(Base):
    """Database Table containing a record of all discovered Comments."""

    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(primary_key=True)  # noqa: A003
    post_id: Mapped[str] = mapped_column(ForeignKey("posts.id"))
    author: Mapped[str | None]
    body: Mapped[str | None]
    permalink: Mapped[str | None]
    created: Mapped[datetime | None]
    notification_sent: Mapped[bool] = mapped_column(server_default=false())

    posts = relationship("DBPosts")
