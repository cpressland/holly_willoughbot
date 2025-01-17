from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Text
from piccolo.columns.column_types import Varchar


ID = "2025-01-17T12:49:45:494289"
VERSION = "1.22.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="holly_willoughbot", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="RedditComments",
        tablename="reddit_comments",
        column_name="body",
        db_column_name="body",
        params={},
        old_params={},
        column_class=Text,
        old_column_class=Varchar,
        schema=None,
    )

    return manager
