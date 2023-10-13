"""Module containing the bot itself."""

from time import sleep

import pendulum
import telebot
from praw import Reddit

from holly_willoughbot.settings import logger, reddit_settings, telegram_settings
from holly_willoughbot.tables import Comments, Posts


class Bot:
    """Main Class for all Bot Features."""

    def __init__(self, first_run: bool, search_limit: int, subreddits: str, lock_age: int) -> None:
        """Initialise the Bot.

        Args:
            first_run (bool): Run the bot for the first time, Avoids spamming telegram.
            search_limit (int): The number of posts to search.
            subreddits (str): The subreddits to search.
            lock_age (int): The age in days of posts to lock.
        """
        self.first_run = first_run
        self.search_limit = search_limit
        self.subreddits = subreddits.split(",")
        self.lock_age = lock_age

        self.reddit = Reddit(
            client_id=reddit_settings.client_id,
            client_secret=reddit_settings.client_secret,
            username=reddit_settings.username,
            password=reddit_settings.password,
            user_agent=reddit_settings.user_agent,
        )

        self.telegram = telebot.TeleBot(token=telegram_settings.token)

    def search_posts(self) -> None:
        """Search Reddit for new Posts and add them to the database."""
        for subreddit in self.subreddits:
            logger.info("Searching Subreddit", extra={"subreddit": subreddit})
            search_limit = self.search_limit if not self.first_run else None
            for post in self.reddit.subreddit(subreddit).new(limit=search_limit):
                already_exists = Posts.exists().where(Posts.post_id == post.id).run_sync()
                if not already_exists:
                    try:
                        logger.info(
                            "Processing Post",
                            extra={"subreddit": subreddit, "post_id": post.id, "title": post.title},
                        )
                        Posts.insert(
                            Posts(
                                post_id=post.id,
                                subreddit=subreddit,
                                title=post.title,
                                author=post.author.name,
                                created=pendulum.from_timestamp(post.created_utc).to_iso8601_string(),
                                locked=post.locked if not post.archived else post.archived,
                                url=f"https://reddit.com{post.permalink}",
                                notified=False,
                            ),
                        ).run_sync()
                    except AttributeError:
                        continue

    def search_comments(self) -> None:
        """Search Reddit Posts for new Comments and add them to the database."""
        posts = Posts.select(Posts.id, Posts.post_id, Posts.subreddit).where(Posts.locked.eq(value=False)).run_sync()
        for post in posts:
            for comment in self.reddit.submission(id=post["post_id"]).comments.list():
                already_exists = Comments.exists().where(Comments.comment_id == comment.id).run_sync()
                logger.info(
                    "Searching Comments",
                    extra={"subreddit": post["subreddit"], "post_id": post["post_id"]},
                )
                if not already_exists and comment.author is not None and comment.author.name != "AutoModerator":
                    logger.info(
                        "Processing Comment",
                        extra={"subreddit": post["subreddit"], "post_id": post["post_id"], "comment": comment.body},
                    )
                    Comments.insert(
                        Comments(
                            comment_id=comment.id,
                            post_id=Posts(id=post["id"]),
                            author=comment.author.name,
                            created=pendulum.from_timestamp(comment.created_utc).to_iso8601_string(),
                            body=comment.body,
                            url=f"https://reddit.com{comment.permalink}",
                            notified=False,
                        ),
                    ).run_sync()

    def nuke_notifications(self) -> None:
        """Flag all posts and comments to notified."""
        if self.first_run:
            logger.info("Marking all Posts and Comments as Notified")
            Posts.update({Posts.notified: True}, force=True).run_sync()
            Comments.update({Comments.notified: True}, force=True).run_sync()

    def lock_posts(self) -> None:
        """Lock Posts that are older than self.lock_age, default 7 days."""
        lock_date = pendulum.now().subtract(days=self.lock_age).timestamp()
        posts = (
            Posts.select(Posts.post_id, Posts.subreddit, Posts.url)
            .where(Posts.locked.eq(value=False), Posts.created < lock_date)
            .run_sync()
        )
        for post in posts:
            logger.info(
                "Locking Post",
                extra={"subreddit": post["subreddit"], "post_id": post["post_id"], "url": post["url"]},
            )
            self.reddit.submission(id=post["post_id"]).mod.lock()
            Posts.update({Posts.locked: True}, force=True).where(Posts.post_id == post["post_id"]).run_sync()

    def _send_message(self, msg: str) -> None:
        msg_fix = str.maketrans(
            {
                ">": "\>",
                "(": "\(",
                ")": "\)",
                "!": "\!",
                "#": "\#",
                "-": "\-",
                "_": "\_",
                ":": "\:",
                ".": "\.",
                "=": "\=",
                "+": "\+",
            },
        )
        try:
            self.telegram.send_message(
                chat_id=telegram_settings.chat_id,
                text=msg.translate(msg_fix),
                parse_mode="MarkdownV2",
                disable_web_page_preview=True,
            )
        except telebot.apihelper.ApiTelegramException as e:
            self.telegram.send_message(
                chat_id=telegram_settings.chat_id,
                text=f"Exception: {e}\n\n Payload: {msg}",
                disable_web_page_preview=True,
            )
        sleep(3)  # Lazy hack to avoid rate limiting

    def notify(self) -> None:
        """Notify Telegram of new Posts and Comments."""
        posts = (
            Posts.select(Posts.post_id, Posts.subreddit, Posts.title, Posts.author, Posts.created, Posts.url)
            .where(Posts.notified.eq(value=False))
            .run_sync()
        )
        for post in posts:
            logger.info(
                "Sending Post Notification",
                extra={"subreddit": post["subreddit"], "post_id": post["post_id"]},
            )
            self._send_message(
                msg=(
                    "*New Post*:\n\n"
                    f"*Title:* {post['title']}\n"
                    f"*Subreddit:* {post['subreddit']}\n"
                    f"*User:* {post['author']}\n"
                    f"*Date:* {post['created']}\n"
                    f"*URL:* {post['url']}"
                ),
            )
            Posts.update({Posts.notified: True}, force=True).where(Posts.post_id == post["post_id"]).run_sync()
        comments = (
            Comments.select(
                Comments.comment_id,
                Comments.post_id.subreddit,
                Comments.post_id.post_id,
                Comments.author,
                Comments.created,
                Comments.body,
                Comments.url,
            )
            .where(Comments.notified.eq(value=False))
            .run_sync()
        )
        for comment in comments:
            logger.info(
                "Sending Comment Notification",
                extra={"subreddit": comment["post_id.subreddit"], "post_id": comment["post_id.post_id"]},
            )
            self._send_message(
                msg=(
                    "*New Comment*:\n\n"
                    f"*Subreddit:* {comment['post_id.subreddit']}\n"
                    f"*User*: {comment['author']}\n"
                    f"*Date*: {comment['created']}\n"
                    f"*URL*: {comment['url']}\n"
                    "*Body*:\n"
                    f"{comment['body']}\n\n"
                ),
            )
            Comments.update({Comments.notified: True}, force=True).where(
                Comments.comment_id == comment["comment_id"],
            ).run_sync()

    def loop(self) -> None:
        """Run the bot in a loop."""
        while True:
            self.search_posts()
            self.search_comments()
            self.nuke_notifications()
            self.lock_posts()
            self.notify()
            sleep(300)
