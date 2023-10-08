"""Module containing the CLI."""

import asyncio

import click
from piccolo.apps.migrations.commands.forwards import forwards as migrate

from holly_willoughbot.bot import Bot


@click.command()
@click.option(
    "--first-run",
    is_flag=True,
    help="Run the bot for the first time, ignores --search-limit and disables notifications. Avoids spamming telegram.",
)
@click.option("--search-limit", default=25, help="Number of posts to search.", show_default=True)
@click.option(
    "--subreddits",
    default="TheHollyWilloughby,Kym_Marsh,rochelle_humes,UnaHealy",
    help="Comma separated list of subreddits to monitor.",
    show_default=True,
)
@click.option("--lock-age", default=7, help="Age of posts to lock.", show_default=True)
def cli(first_run: bool, search_limit: int, subreddits: str, lock_age: int) -> None:
    """Run the CLI."""
    bot = Bot(
        first_run=first_run,
        search_limit=search_limit,
        subreddits=subreddits,
        lock_age=lock_age,
    )
    asyncio.run(migrate(app_name="holly_willoughbot"))
    bot.loop()


cli(max_content_width=256)
