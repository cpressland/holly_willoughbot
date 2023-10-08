"""Module containing database tables."""
from piccolo.columns import Boolean, ForeignKey, Text, Timestamptz
from piccolo.table import Table


class Posts(Table):
    """Database Table: Reddit Posts."""

    post_id = Text()
    subreddit = Text()
    title = Text()
    author = Text()
    created = Timestamptz()
    locked = Boolean()
    url = Text()
    notified = Boolean(default=False)


class Comments(Table):
    """Database Table: Reddit Comments."""

    comment_id = Text()
    post_id = ForeignKey(references=Posts)
    author = Text()
    created = Timestamptz()
    body = Text()
    url = Text()
    notified = Boolean(default=False)
