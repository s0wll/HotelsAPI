"""add rooms

Revision ID: 4ffb1c8c01fc
Revises: eb6393bf49b0
Create Date: 2025-02-01 17:03:14.799846

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4ffb1c8c01fc"
down_revision: Union[str, None] = "eb6393bf49b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
