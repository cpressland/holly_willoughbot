"""Database Migration Module."""

from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns import Boolean, ForeignKey, Text, Timestamptz

ID = "2023-10-08T14:14:20:582907"
VERSION = "0.121.0"
DESCRIPTION = "Initial Database Schema."


async def forwards() -> MigrationManager:
    """Move Database Forward."""
    manager = MigrationManager(migration_id=ID, app_name="holly_willoughbot", description=DESCRIPTION)

    manager.add_table("Posts", tablename="posts")

    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="post_id",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="subreddit",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="title",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="author",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="created",
        column_class=Timestamptz,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="locked",
        column_class=Boolean,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="url",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Posts",
        tablename="posts",
        column_name="notified",
        column_class=Boolean,
    )

    manager.add_table("Comments", tablename="comments")
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="comment_id",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="post_id",
        column_class=ForeignKey,
        params={
            "references": "posts",
        },
    )
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="author",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="created",
        column_class=Timestamptz,
    )
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="body",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="url",
        column_class=Text,
    )
    manager.add_column(
        table_class_name="Comments",
        tablename="comments",
        column_name="notified",
        column_class=Boolean,
    )

    return manager
