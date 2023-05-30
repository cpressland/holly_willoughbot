import telebot
from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from holly_willoughbot.database import DB_Comments, DB_Posts, engine
from holly_willoughbot.settings import settings


class TelegramNotifications:
    MSG_REPLACEMENTS = str.maketrans(
        {">": "\>", "(": "\(", ")": "\)", "!": "\!", "#": "\#", "-": "\-", "_": "\_", ":": "\:", ".": "\."}
    )

    def __init__(self) -> None:
        self.chat_id = "-820505138"
        self.bot = telebot.TeleBot(token=settings.telegram_token)

    def send_msg(self, text: str) -> None:
        if settings.notifications_enabled:
            try:
                logger.warning(f"Sending Notification: {text}")
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=text.translate(TelegramNotifications.MSG_REPLACEMENTS),
                    parse_mode="MarkdownV2",
                    disable_web_page_preview=True,
                )
            except telebot.apihelper.ApiTelegramException as e:
                self.bot.send_message(
                    chat_id=self.chat_id,
                    text=f"Exception: {e}\n\n Payload: {text}",
                    disable_web_page_preview=True,
                )

    def notify(self) -> None:
        logger.warning("Beginning Notification Run")
        with Session(engine) as session:
            posts = session.execute(select(DB_Posts).where(DB_Posts.notification_sent.is_(False)))
            for (post,) in posts:
                self.send_msg(
                    text=(
                        "*New Post*:\n\n"
                        f"*Title:* {post.title}\n"
                        f"*User:* {post.author}\n"
                        f"*Date:* {post.created}\n"
                        f"*URL:* http://www.reddit.com{post.permalink}"
                    )
                )
                session.execute(update(DB_Posts).where(DB_Posts.id == post.id).values(notification_sent=True))
            session.commit()

            comments = session.execute(select(DB_Comments).where(DB_Comments.notification_sent.is_(False)))
            for (comment,) in comments:
                self.send_msg(
                    text=(
                        "*New Comment*:\n\n"
                        f"*User*: {comment.author}\n"
                        f"*Date*: {comment.created}\n"
                        f"*URL*: http://www.reddit.com{comment.permalink}\n"
                        "*Body*:\n"
                        f"{comment.body}\n\n"
                    )
                )
                session.execute(update(DB_Comments).where(DB_Comments.id == comment.id).values(notification_sent=True))
            session.commit()
