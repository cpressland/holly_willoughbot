"""holly_willoughbot Package."""

import typer

cli = typer.Typer(no_args_is_help=True)


@cli.command()
def task_loop() -> None:
    """Run the scrape, lock, and notify tasks in a loop."""
    import asyncio
    from time import sleep

    from piccolo.apps.migrations.commands.forwards import forwards as migrate

    from holly_willoughbot.tasks import lock, notify, scrape

    asyncio.run(migrate(app_name="session_auth"))
    asyncio.run(migrate(app_name="user"))
    asyncio.run(migrate(app_name="holly_willoughbot"))

    while True:
        scrape()
        lock()
        notify()
        sleep(60)


@cli.command()
def scrape() -> None:
    """Scrape Reddit for new submissions and comments."""
    from holly_willoughbot.tasks import scrape as run_scrape

    run_scrape()


@cli.command()
def lock() -> None:
    """Lock submissions older than a week."""
    from holly_willoughbot.tasks import lock as run_lock

    run_lock()


@cli.command()
def notify() -> None:
    """Send Notifications for new submissions and comments."""
    from holly_willoughbot.tasks import notify as run_notify

    run_notify()


@cli.command()
def server(host: str = "127.0.0.1", port: int = 6502) -> None:
    """Run the API Server, which provides an Admin interface."""
    import uvicorn

    uvicorn.run("holly_willoughbot.api:api", host=host, port=port)


@cli.command()
def migrate() -> None:
    """Run the migrations."""
    import asyncio

    from piccolo.apps.migrations.commands.forwards import forwards

    asyncio.run(forwards(app_name="session_auth"))
    asyncio.run(forwards(app_name="user"))
    asyncio.run(forwards(app_name="holly_willoughbot"))
