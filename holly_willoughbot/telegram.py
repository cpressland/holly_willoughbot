"""Telegram API functions."""

import telebot

from holly_willoughbot.tables import TelegramClients


def send_message(message: str, client_id: int) -> None:
    """Send a message to the Telegram chat.

    Args:
        message (str): The message to send.
        client_id (int): The Telegram client to send the message from.

    """
    client = TelegramClients.objects().get(TelegramClients.id == client_id).run_sync()
    telegram = telebot.TeleBot(token=client.token)
    translations = str.maketrans(
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
            "|": "\|",
        },
    )
    try:
        telegram.send_message(
            chat_id=client.chat_id,
            text=message.translate(translations),
            parse_mode="MarkdownV2",
            disable_web_page_preview=True,
        )
    except telebot.apihelper.ApiTelegramException as e:
        telegram.send_message(
            chat_id=client.chat_id,
            text=f"Exception: {e}\n\n Payload: {message}",
            disable_web_page_preview=True,
        )
