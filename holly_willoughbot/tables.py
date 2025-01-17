"""Database Table definitions."""

from piccolo.columns import Boolean, ForeignKey, Integer, Secret, Text, Timestamptz, Varchar
from piccolo.columns.readable import Readable
from piccolo.table import Table


class TelegramClients(Table, tablename="telegram_clients"):
    """Telegram Clients.

    Attributes:
        friendly_name (Varchar): The name of the chat.
        chat_id (Varchar): The chat ID.
        token (Varchar): The secret for the chat.

    """

    friendly_name = Varchar(unique=True)
    chat_id = Varchar(unique=True)
    token = Secret()

    @classmethod
    def get_readable(cls) -> Readable:
        """Return a human readable representation of the foreign key in Piccolo Admin."""
        return Readable(template="%s", columns=[cls.friendly_name])


class RedditClients(Table, tablename="reddit_clients"):
    """Reddit Clients.

    Attributes:
        client_id (Varchar): The client ID.
        client_secret (Varchar): The client secret.
        username (Varchar): The username.
        password (Secret): The password.

    """

    client_id = Varchar(unique=True)
    client_secret = Secret()
    username = Varchar()
    password = Secret()

    @classmethod
    def get_readable(cls) -> Readable:
        """Return a human readable representation of the foreign key in Piccolo Admin."""
        return Readable(template="%s", columns=[cls.username])


class RedditSubreddits(Table, tablename="reddit_subreddits"):
    """Reddit Subreddits.

    Attributes:
        subreddit (Varchar): The subreddit name.
        enabled (Boolean): Whether the subreddit is enabled.
        muted (Boolean): Whether notifications for the subreddit are muted or not.
        search_limit (Integer): The number of posts to search.
        first_scrape_complete (Boolean): Whether the first scrape of the subreddit has been completed.

    """

    subreddit = Varchar(unique=True)
    enabled = Boolean(default=True)
    muted = Boolean(default=False)
    search_limit = Integer(default=25)
    first_scrape_complete = Boolean(default=False)
    reddit_client = ForeignKey(references=RedditClients)
    telegram_client = ForeignKey(references=TelegramClients)

    @classmethod
    def get_readable(cls) -> Readable:
        """Return a human readable representation of the foreign key in Piccolo Admin."""
        return Readable(template="%s", columns=[cls.subreddit])


class RedditSubmissions(Table, tablename="reddit_submissions"):
    """Reddit Submissions.

    Attributes:
        submission_id (Varchar): The Reddit post ID.
        subreddit (Varchar): The subreddit the post was submitted to.
        title (Varchar): The title of the post.
        author (Varchar): The author of the post.
        created (Timestamptz): The creation date of the post.
        locked (Boolean): Whether the post is locked.
        url (Varchar): The URL of the post.
        notified (Boolean): Whether the post has been notified.

    """

    submission_id = Varchar(unique=True)
    subreddit = ForeignKey(references=RedditSubreddits)
    title = Varchar()
    author = Varchar()
    created = Timestamptz()
    locked = Boolean()
    url = Varchar()
    notified = Boolean(default=False)

    @classmethod
    def get_readable(cls) -> Readable:
        """Return a human readable representation of the foreign key in Piccolo Admin."""
        return Readable(template="%s", columns=[cls.title])


class RedditComments(Table, tablename="reddit_comments"):
    """Reddit Comments.

    Attributes:
        comment_id (Varchar): The Reddit comment ID.
        submission_id (ForeignKey): The Reddit post ID.
        author (Varchar): The author of the comment.
        created (Timestamptz): The creation date of the comment.
        body (Text): The body of the comment.
        url (Varchar): The URL of the comment.
        notified (Boolean): Whether the comment has been notified.

    """

    comment_id = Varchar(unique=True)
    submission_id = ForeignKey(references=RedditSubmissions)
    subreddit = ForeignKey(references=RedditSubreddits)
    author = Varchar()
    created = Timestamptz()
    body = Text()
    url = Varchar()
    notified = Boolean(default=False)
