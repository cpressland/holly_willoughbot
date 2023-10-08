"""Piccolo Config Module."""

from piccolo.conf.apps import AppRegistry
from piccolo.engine.sqlite import SQLiteEngine

from holly_willoughbot.settings import database_settings

DB = SQLiteEngine(path=database_settings.path)
APP_REGISTRY = AppRegistry(apps=["holly_willoughbot.piccolo_app"])
