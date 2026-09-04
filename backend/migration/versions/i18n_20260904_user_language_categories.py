"""add user language and default category keys

Revision ID: i18n20260904
Revises: c20260904cur
Create Date: 2026-09-04 21:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'i18n20260904'
down_revision: Union[str, None] = 'c20260904cur'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('language', sa.String(length=8), nullable=True))
    op.add_column('category', sa.Column('default_key', sa.String(), nullable=True))
    op.add_column('category', sa.Column('is_default', sa.Boolean(), nullable=False, server_default=sa.text('false')))

    mappings = [
        ('outcome', 'Transport', 'transport'),
        ('outcome', 'Food & Dining', 'food_dining'),
        ('outcome', 'Shopping', 'shopping'),
        ('outcome', 'Healthcare', 'healthcare'),
        ('outcome', 'Education', 'education'),
        ('outcome', 'Travel', 'travel'),
        ('outcome', 'Entertainment', 'entertainment'),
        ('outcome', 'Utilities', 'utilities'),
        ('outcome', 'Gifts', 'gifts'),
        ('outcome', 'Savings', 'savings'),
        ('outcome', 'Rent', 'rent'),
        ('outcome', 'Loans', 'loans'),
        ('outcome', 'Subscriptions', 'subscriptions'),
        ('outcome', 'Hobbies', 'hobbies'),
        ('outcome', 'Investments', 'investments'),
        ('outcome', 'Miscellaneous', 'miscellaneous'),
        ('income', 'Salary', 'salary'),
        ('income', 'Freelance', 'freelance'),
        ('income', 'Side Hustle', 'side_hustle'),
        ('income', 'Investments', 'income_investments'),
        ('income', 'Gifts & Bonuses', 'gifts_bonuses'),
        ('income', 'Property Sale', 'property_sale'),
        ('income', 'Rental Income', 'rental_income'),
        ('income', 'Miscellaneous', 'income_miscellaneous'),
    ]
    for transaction_type, name, default_key in mappings:
        op.execute(
            sa.text("""
                UPDATE category
                SET default_key = :default_key, is_default = true
                WHERE transaction_type = :transaction_type AND name = :name
            """).bindparams(default_key=default_key, transaction_type=transaction_type, name=name)
        )


def downgrade() -> None:
    op.drop_column('category', 'is_default')
    op.drop_column('category', 'default_key')
    op.drop_column('user', 'language')
