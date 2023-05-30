import click
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
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


@cli.command(name="cron")
def cron() -> None:
    discovery = Discovery()
    notifications = TelegramNotifications()
    locks = ThreadLock()
    scheduler = BlockingScheduler()
    scheduler.add_job(discovery.posts, "interval", minutes=5)
    scheduler.add_job(discovery.comments, "interval", minutes=5)
    scheduler.add_job(notifications.notify, "interval", minutes=1)
    scheduler.add_job(locks.lock, trigger=CronTrigger.from_crontab("10 0 * * *"))
    scheduler.start()
