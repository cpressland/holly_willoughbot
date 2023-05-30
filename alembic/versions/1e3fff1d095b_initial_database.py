"""Initial Database

Revision ID: 1e3fff1d095b
Revises: 
Create Date: 2023-05-29 18:17:30.052214

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "1e3fff1d095b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("subreddit", sa.String),
        sa.Column("title", sa.String),
        sa.Column("author", sa.String),
        sa.Column("created", sa.DateTime),
        sa.Column("permalink", sa.String),
        sa.Column("locked", sa.Boolean),
        sa.Column("notification_sent", sa.Boolean, server_default=sa.false(), nullable=False),
    )
    op.create_table(
        "comments",
        sa.Column("id", sa.String, primary_key=False),
        sa.Column("post_id", sa.String, sa.ForeignKey("posts.id", ondelete="CASCADE")),
        sa.Column("author", sa.String),
        sa.Column("body", sa.String),
        sa.Column("notification_sent", sa.Boolean, server_default=sa.false(), nullable=False),
    )


def downgrade() -> None:
    pass
