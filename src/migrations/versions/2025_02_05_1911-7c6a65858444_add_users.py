"""add users

Revision ID: 7c6a65858444
Revises: 4ffb1c8c01fc
Create Date: 2025-02-05 19:11:42.311036

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7c6a65858444"
down_revision: Union[str, None] = "4ffb1c8c01fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
