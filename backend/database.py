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
    name = Optional(str)
    currency = Required('Currency')
    categories = Set('Category')


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    transactions = Set('Transaction')
    name = Optional(str)
    wallet = Required(Wallet)
    transaction_type = Required('TransactionType')


class Transaction(db.Entity):
    id = PrimaryKey(int, auto=True)
    category = Required(Category)
    description = Optional(str)
    value = Optional(Decimal)
    wallet = Required(Wallet)
    date = Optional(datetime)
    source = Optional(str)


class User2Wallet(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    wallet = Required(Wallet)
    user_type = Optional(str)


class TransactionType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    categories = Set(Category)


class Currency(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    wallets = Set(Wallet)
