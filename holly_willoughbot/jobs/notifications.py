"""Module Containing Notification Features."""
from time import sleep

import telebot
from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from holly_willoughbot.database import DBComments, DBPosts, engine
from holly_willoughbot.settings import settings


class TelegramNotifications:
    """Send Notifications to Telegram."""

    MSG_REPLACEMENTS = str.maketrans(
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
        },
    )

    def __init__(self) -> None:
        """Initialize the TelegramNotifications Class."""
        self.chat_id = "-820505138"
        self.bot = telebot.TeleBot(token=settings.telegram_token)

    def send_msg(self, text: str) -> None:
        """If notifications are enabled, send a message to Telegram.

        Args:
            text (str): The message to send.
        """
        if settings.notifications_enabled:
            try:
                logger.warning(f"Sending Notification: {text}")
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=text.translate(TelegramNotifications.MSG_REPLACEMENTS),
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True,
                )
                sleep(5)
            except telebot.apihelper.ApiTelegramException as e:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"Exception: {e}\n\n Payload: {text}",
                    disable_web_page_preview=True,
                )

    def notify(self) -> None:
        """Scan database for pending notifications and send them."""
        logger.warning("Beginning Notification Run")
        with Session(engine) as session:
            posts = session.execute(select(DBPosts).where(DBPosts.notification_sent.is_(False)))
            for (post,) in posts:
                self.send_msg(
                    text=(
                        "*New Post*:\n\n"
                        f"*Title:* {post.title}\n"
                        f"*User:* {post.author}\n"
                        f"*Date:* {post.created}\n"
                        f"*URL:* http://www.reddit.com{post.permalink}"
                    ),
                )
                session.execute(update(DBPosts).where(DBPosts.id == post.id).values(notification_sent=True))
            session.commit()

            comments = session.execute(select(DBComments).where(DBComments.notification_sent.is_(False)))
            for (comment,) in comments:
                self.send_msg(
                    text=(
                        "*New Comment*:\n\n"
                        f"*User*: {comment.author}\n"
                        f"*Date*: {comment.created}\n"
                        f"*URL*: http://www.reddit.com{comment.permalink}\n"
                        "*Body*:\n"
                        f"{comment.body}\n\n"
                    ),
                )
                session.execute(update(DBComments).where(DBComments.id == comment.id).values(notification_sent=True))
            session.commit()
