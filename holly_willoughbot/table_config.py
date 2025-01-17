"""Piccolo Admin Table Config."""

from piccolo_admin.endpoints import TableConfig

from holly_willoughbot.tables import RedditClients, RedditComments, RedditSubmissions, RedditSubreddits, TelegramClients

telegram_clients = TableConfig(
    TelegramClients,
    menu_group="Telegram",
    link_column=TelegramClients.friendly_name,
    visible_columns=[
        TelegramClients.friendly_name,
        TelegramClients.chat_id,
    ],
)

reddit_clients = TableConfig(
    RedditClients,
    menu_group="Reddit",
    link_column=RedditClients.username,
    visible_columns=[
        RedditClients.username,
        RedditClients.client_id,
    ],
)

reddit_subreddits = TableConfig(
    RedditSubreddits,
    menu_group="Reddit",
    link_column=RedditSubreddits.subreddit,
    visible_columns=[
        RedditSubreddits.subreddit,
        RedditSubreddits.enabled,
        RedditSubreddits.muted,
        RedditSubreddits.search_limit,
        RedditSubreddits.first_scrape_complete,
    ],
)

reddit_submissions = TableConfig(
    RedditSubmissions,
    menu_group="Reddit",
    link_column=RedditSubmissions.title,
    visible_columns=[
        RedditSubmissions.title,
        RedditSubmissions.author,
        RedditSubreddits.subreddit,
        RedditSubmissions.created,
        RedditSubmissions.locked,
        RedditSubmissions.notified,
    ],
)

reddit_comments = TableConfig(
    RedditComments,
    menu_group="Reddit",
    link_column=RedditComments.body,
    visible_columns=[
        RedditSubreddits.subreddit,
        RedditComments.author,
        RedditComments.body,
    ],
)
