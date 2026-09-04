"""add default wallet

Revision ID: 7b4d17a2f8c1
Revises: 267c95e77395
Create Date: 2026-09-04 16:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7b4d17a2f8c1'
down_revision: Union[str, None] = '267c95e77395'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('default_wallet', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_user_default_wallet_wallet', 'user', 'wallet', ['default_wallet'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_user_default_wallet_wallet', 'user', type_='foreignkey')
    op.drop_column('user', 'default_wallet')
