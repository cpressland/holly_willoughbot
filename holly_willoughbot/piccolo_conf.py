"""Piccolo Config Module."""

from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from holly_willoughbot.settings import settings

DB = PostgresEngine(config={"dsn": str(settings.database_url)})
APP_REGISTRY = AppRegistry(apps=["holly_willoughbot.piccolo_app", "piccolo_admin.piccolo_app"])
