"""refactor users model

Revision ID: fbbdcd0d91f1
Revises: 7c6a65858444
Create Date: 2025-02-05 20:59:02.292259

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "fbbdcd0d91f1"
down_revision: Union[str, None] = "7c6a65858444"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
