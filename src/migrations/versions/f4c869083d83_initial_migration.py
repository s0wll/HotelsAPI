"""initial migration

Revision ID: f4c869083d83
Revises: f3dd2ffccc41
Create Date: 2025-02-01 16:10:25.537288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f4c869083d83'
down_revision: Union[str, None] = 'f3dd2ffccc41'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('rooms')
