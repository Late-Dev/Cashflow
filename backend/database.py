from datetime import datetime
from decimal import Decimal
from pony.orm import *

from default_categories import default_categories


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    user2_wallets = Set('User2Wallet')
    transactions = Set('Transaction')


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
    icon = Optional(str)
    color = Optional(int)


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    category = Required(Category)
    description = Optional(str)
    value = Required(Decimal)
    wallet = Required(Wallet)
    date = Required(datetime)
    source = Optional(str)
    user = Required(User)


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

    if(len(wallets) < 1):
        add_user_data({'id': id})
        add_wallet_data({'user_id': id, 'name': 'Personal wallet', 'currency': "USD"})

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
        transaction_type=category['transaction_type'],
        icon=category['icon'],
        color=category['color'],
    )

@db_session
def delete_category_data(id: int):
    Category[id].delete()

@db_session
def update_category_data(id: int, category: dict):
    current_category = Category[id]
    current_category.name = category.get('name', None) or current_category.name
    current_category.icon = category.get('icon', None) or current_category.icon
    current_category.color = category.get('color', None) or current_category.color

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
    for category in default_categories:
        Category(
            name=category['name'],
            wallet=wallet,
            transaction_type=category['transaction_type'],
            icon=category['icon'],
            color=category['color'],
        )

@db_session
def delete_wallet_data(id: int):
    Wallet[id].delete()

@db_session
def update_wallet_data(id: int, wallet: dict):
    current_wallet = Wallet[id]
    current_wallet.name = wallet.get('name', None) or current_wallet.name

@db_session
def add_transaction_data(transaction: dict):
    category = Category[transaction['category_id']]
    wallet = Wallet[transaction['wallet_id']]
    date = datetime.fromisoformat(transaction['date'])
    user = User[transaction['user_id']]
    Transaction(
        category=category,
        description=transaction['description'],
        value=transaction['value'],
        wallet=wallet,
        source=transaction['source'],
        date=date,
        user=user
    )

@db_session
def delete_transaction_data(id: int):
    Transaction[id].delete()

@db_session
def update_transaction_data(id: int, transaction: dict):
    current_transaction = Transaction[id]
    if transaction.get('category_id', None) is not None:
        current_transaction.category = Category[transaction['category_id']]
    current_transaction.description = transaction.get('description', None) or current_transaction.description
    current_transaction.value = transaction.get('value', None) or current_transaction.value
    current_transaction.date = transaction.get('date', None) or current_transaction.date
    current_transaction.source = transaction.get('source', None) or current_transaction.source

