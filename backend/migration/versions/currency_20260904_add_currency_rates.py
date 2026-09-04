"""add currencies and rates

Revision ID: c20260904cur
Revises: 7b4d17a2f8c1
Create Date: 2026-09-04 17:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c20260904cur'
down_revision: Union[str, None] = '7b4d17a2f8c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'currency',
        sa.Column('code', sa.String(length=3), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('symbol', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('code'),
    )
    op.create_table(
        'currency_rate',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('usd_to_currency', sa.Numeric(precision=18, scale=8), nullable=False),
        sa.ForeignKeyConstraint(['currency'], ['currency.code']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('currency', 'date', name='uq_currency_rate_currency_date'),
    )
    op.add_column('wallet', sa.Column('default_currency', sa.String(length=3), nullable=True))
    op.add_column('transaction', sa.Column('currency', sa.String(length=3), nullable=True))
    op.add_column('transaction', sa.Column('usd_to_currency_rate', sa.Numeric(precision=18, scale=8), nullable=True))

    currencies = [
        {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
        {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
        {'code': 'RUB', 'name': 'Russian Ruble', 'symbol': '₽'},
        {'code': 'KGS', 'name': 'Kyrgyzstani Som', 'symbol': 'сом'},
        {'code': 'KZT', 'name': 'Kazakhstani Tenge', 'symbol': '₸'},
        {'code': 'UZS', 'name': 'Uzbekistani Som', 'symbol': "so'm"},
        {'code': 'CNY', 'name': 'Chinese Yuan', 'symbol': '¥'},
        {'code': 'GBP', 'name': 'British Pound', 'symbol': '£'},
        {'code': 'TRY', 'name': 'Turkish Lira', 'symbol': '₺'},
        {'code': 'AED', 'name': 'UAE Dirham', 'symbol': 'د.إ'},
    ]
    op.bulk_insert(sa.table('currency',
        sa.column('code', sa.String),
        sa.column('name', sa.String),
        sa.column('symbol', sa.String),
    ), currencies)

    op.execute("UPDATE wallet SET default_currency = COALESCE(NULLIF(currency, ''), 'USD')")
    op.execute("UPDATE transaction SET currency = 'USD', usd_to_currency_rate = 1 WHERE currency IS NULL")

    op.alter_column('wallet', 'default_currency', nullable=False)
    op.alter_column('transaction', 'currency', nullable=False)
    op.alter_column('transaction', 'usd_to_currency_rate', nullable=False)
    op.create_foreign_key('fk_wallet_default_currency_currency', 'wallet', 'currency', ['default_currency'], ['code'])
    op.create_foreign_key('fk_transaction_currency_currency', 'transaction', 'currency', ['currency'], ['code'])


def downgrade() -> None:
    op.drop_constraint('fk_transaction_currency_currency', 'transaction', type_='foreignkey')
    op.drop_constraint('fk_wallet_default_currency_currency', 'wallet', type_='foreignkey')
    op.drop_column('transaction', 'usd_to_currency_rate')
    op.drop_column('transaction', 'currency')
    op.drop_column('wallet', 'default_currency')
    op.drop_table('currency_rate')
    op.drop_table('currency')
