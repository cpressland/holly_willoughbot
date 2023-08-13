"""Add Permalink to Comments Table.

Revision ID: aa2ba21988cc
Revises: 7fb17d8d81d9
Create Date: 2023-05-30 17:29:05.130721

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "aa2ba21988cc"
down_revision = "7fb17d8d81d9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add a permalink column to comments table."""
    op.add_column(
        "comments",
        sa.Column("permalink", sa.String),
    )


def downgrade() -> None:
    """Remove the permalink column from comments table."""
    op.drop_column("comments", "permalink")
