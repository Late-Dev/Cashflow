from datetime import datetime
from decimal import Decimal
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user2_wallets = Set('User2Wallet')


class Wallet(db.Entity):
    id = PrimaryKey(int, auto=True)
    user2_wallets = Set('User2Wallet')
    transactions = Set('Transaction')
    name = Required(str)
    categories = Set('Category')
    currency = Required(str)


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    transactions = Set('Transaction')
    name = Required(str)
    wallet = Required(Wallet)
    transaction_type = Optional(str)


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    category = Required(Category)
    description = Optional(str)
    value = Required(Decimal)
    wallet = Required(Wallet)
    date = Required(datetime)
    source = Optional(str)


class User2Wallet(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    wallet = Required(Wallet)
    user_type = Required(str)


@db_session
def get_wallet_transactions_data(id: int):
    all_transactions = Wallet[id].transactions
    transaction_types = select(c.transaction_type for c in Category if c.wallet.id == id)
    result = {
        transaction_type: [
            transaction.to_dict()
            for transaction in all_transactions 
            if transaction.category.transaction_type == transaction_type
        ] 
        for transaction_type in transaction_types
    }
    return result

@db_session
def get_wallet_categories_data(id: int):
    categories = [category.to_dict() for category in Wallet[id].categories]
    return categories

@db_session
def get_user_wallets_data(id: int):
    wallets = [
        {
            **line.wallet.to_dict(), 
            'user_type': line.user_type
        }
        for line in select(line for line in User2Wallet if line.user.id == id)
    ]
    return wallets

@db_session
def add_user_data(user: dict):
    User(id=user['id'])

@db_session
def add_category_data(category: dict):
    wallet = Wallet[category['wallet_id']]
    Category(
        name=category['name'],
        wallet=wallet,
        transaction_type=category['transaction_type']
    )

@db_session
def add_wallet_data(wallet: dict):
    user = User[wallet['user_id']]
    wallet = Wallet(
        name=wallet['name'],
        currency=wallet['currency']
    )
    User2Wallet(
        user=user,
        wallet=wallet,
        user_type='owner'
    )

@db_session
def add_transaction_data(transaction: dict):
    category = Category[transaction['category_id']]
    wallet = Wallet[transaction['wallet_id']]
    date = datetime.fromisoformat(transaction['date'])
    Transaction(
        category=category,
        description=transaction['description'],
        value=transaction['value'],
        wallet=wallet,
        source=transaction['source'],
        date=date,
    )