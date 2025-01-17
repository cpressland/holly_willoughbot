"""Import all of the Tables subclasses in your app here, and register them with the APP_CONFIG."""

from piccolo.conf.apps import AppConfig, table_finder

APP_CONFIG = AppConfig(
    app_name="holly_willoughbot",
    migrations_folder_path="holly_willoughbot/migrations",
    table_classes=table_finder(modules=["holly_willoughbot.tables"], exclude_imported=True),
    migration_dependencies=[],
    commands=[],
)
