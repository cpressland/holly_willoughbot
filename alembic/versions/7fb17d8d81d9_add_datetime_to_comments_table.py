"""Add DateTime to Comments Table

Revision ID: 7fb17d8d81d9
Revises: 1e3fff1d095b
Create Date: 2023-05-30 17:20:06.952461

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7fb17d8d81d9"
down_revision = "1e3fff1d095b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "comments",
        sa.Column("created", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_column("comments", "created")
