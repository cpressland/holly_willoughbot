import click
from trogon import tui

from holly_willoughbot.jobs.discovery import Discovery
from holly_willoughbot.jobs.lock import ThreadLock
from holly_willoughbot.jobs.notifications import TelegramNotifications


@tui()
@click.group()
def cli() -> None:
    pass


@cli.command(name="notifications")
def notifications():
    job = TelegramNotifications()
    job.notify()


@cli.command(name="discovery")
def discovery() -> None:
    job = Discovery()
    job.posts()
    job.comments()


@cli.command(name="lock")
def lock() -> None:
    job = ThreadLock()
    job.lock()
