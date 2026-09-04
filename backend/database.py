import os
import requests
from datetime import date, datetime
from decimal import Decimal
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Numeric, DateTime

from default_categories import default_categories

logger = logging.getLogger(__name__)


postgres_user = os.environ["POSTGRES_USER"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_host = os.environ["POSTGRES_HOST"]
postgres_database = os.environ["POSTGRES_DB"]

max_attempts = 5

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_database}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    __abstract__ = True
    def to_dict(self):
        return {
            field.name : getattr(self, field.name) 
            for field in self.__table__.c
        }


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    default_wallet = Column(Integer, ForeignKey("wallet.id"), nullable=True)

    user2_wallets = relationship("User2Wallet", back_populates="user_object")
    transactions = relationship("Transaction", back_populates="user_object")


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    default_currency = Column(String(3), ForeignKey("currency.code"), nullable=False, default="USD")

    user2_wallets = relationship("User2Wallet", back_populates="wallet_object")
    transactions = relationship("Transaction", back_populates="wallet_object")
    categories = relationship("Category", back_populates="wallet_object")


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(Integer, nullable=True)
    transaction_type = Column(String, nullable=True)

    wallet = Column(Integer, ForeignKey("wallet.id"))
    wallet_object = relationship("Wallet", back_populates="categories")

    transactions = relationship("Transaction", back_populates="category_object")


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=True)
    value = Column(Numeric(12, 2), nullable=False)
    date = Column(DateTime, nullable=False)
    source = Column(String, nullable=True)
    currency = Column(String(3), ForeignKey("currency.code"), nullable=False, default="USD")
    usd_to_currency_rate = Column(Numeric(18, 8), nullable=False, default=1)

    category = Column(Integer, ForeignKey("category.id"))
    category_object = relationship("Category", back_populates="transactions")

    wallet = Column(Integer, ForeignKey("wallet.id"))
    wallet_object = relationship("Wallet", back_populates="transactions")

    user = Column(Integer, ForeignKey("user.id"))
    user_object = relationship("User", back_populates="transactions")


class User2Wallet(Base):
    __tablename__ = "user2wallet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_type = Column(String, nullable=False)

    user = Column(Integer, ForeignKey("user.id"))
    user_object = relationship("User", back_populates="user2_wallets")

    wallet = Column(Integer, ForeignKey("wallet.id"))
    wallet_object = relationship("Wallet", back_populates="user2_wallets")


class Currency(Base):
    __tablename__ = "currency"

    code = Column(String(3), primary_key=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)


class CurrencyRate(Base):
    __tablename__ = "currency_rate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    currency = Column(String(3), ForeignKey("currency.code"), nullable=False)
    date = Column(Date, nullable=False)
    usd_to_currency = Column(Numeric(18, 8), nullable=False)


EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
DEFAULT_CURRENCY = "USD"


def get_wallet_transactions_data(id: int):
    with Session() as session:
        wallet = session.query(Wallet).filter_by(id=id).first()
        display_currency = wallet.default_currency if wallet else DEFAULT_CURRENCY
        all_transactions = session.query(Transaction).filter_by(wallet=id)
        transaction_types = [
            transaction_type[0]
            for transaction_type in session.query(Category.transaction_type).filter(Category.wallet == id).distinct()
        ]

        def format_transaction(transaction: Transaction):
            transaction_data = transaction.to_dict()
            usd_value = Decimal(transaction.value) / Decimal(transaction.usd_to_currency_rate)
            display_rate = get_currency_rate_data(display_currency, transaction.date.date())
            display_value = usd_value * Decimal(display_rate)
            transaction_data['usd_value'] = round(usd_value, 2)
            transaction_data['display_value'] = round(display_value, 2)
            transaction_data['display_currency'] = display_currency
            return transaction_data

        result = {
            transaction_type: [
                format_transaction(transaction)
                for transaction in all_transactions 
                if transaction.category_object.transaction_type == transaction_type
            ] 
            for transaction_type in transaction_types
        }
    return result

def get_wallet_categories_data(id: int):
    with Session() as session:
        categories = [
            category.to_dict() 
            for category in session.query(Category).filter(Category.wallet == id)
        ]
    return categories

def get_currencies_data():
    with Session() as session:
        return [currency.to_dict() for currency in session.query(Currency).order_by(Currency.code.asc())]

def get_currency_rate_data(currency: str, rate_date: date | None = None) -> Decimal:
    currency = (currency or DEFAULT_CURRENCY).upper()
    rate_date = rate_date or date.today()
    if currency == DEFAULT_CURRENCY:
        return Decimal("1")

    with Session() as session:
        def find_rate(target_date: date):
            return (
                session.query(CurrencyRate)
                .filter(CurrencyRate.currency == currency, CurrencyRate.date == target_date)
                .first()
            )

        existing_rate = find_rate(rate_date)
        if existing_rate:
            return existing_rate.usd_to_currency

        today = date.today()
        today_rate = find_rate(today)
        if today_rate:
            return today_rate.usd_to_currency

        any_today_rate = (
            session.query(CurrencyRate)
            .filter(CurrencyRate.date == today)
            .first()
        )
        if any_today_rate:
            raise ValueError(f'Currency rate for {currency} is not available in today cache')

        if not EXCHANGE_RATE_API_KEY:
            raise ValueError('EXCHANGE_RATE_API_KEY is not configured')

        logger.info("Loading today's currency rates from ExchangeRate API")
        response = requests.get(EXCHANGE_RATE_API_URL.format(api_key=EXCHANGE_RATE_API_KEY), timeout=10)
        response.raise_for_status()
        conversion_rates = response.json().get('conversion_rates', {})

        supported_codes = [code for code, in session.query(Currency.code).all()]
        for code in supported_codes:
            rate = conversion_rates.get(code)
            if rate is None:
                continue
            session.add(CurrencyRate(
                currency=code,
                date=today,
                usd_to_currency=Decimal(str(rate)),
            ))
        session.commit()

        refreshed_rate = find_rate(today)
        if refreshed_rate:
            return refreshed_rate.usd_to_currency

    raise ValueError(f'Currency rate for {currency} is not available')

def get_user_wallets_data(id: int):
    with Session() as session:
        user = session.query(User).filter(User.id == id).first()
        wallets = [
            {
                **line.wallet_object.to_dict(), 
                'user_type': line.user_type,
                'is_default': user.default_wallet == line.wallet if user and user.default_wallet else False
            }
            for line in session.query(User2Wallet).filter(User2Wallet.user == id)
        ]
        if(len(wallets) < 1):
            add_wallet_data({'user_id': id, 'name': 'Personal wallet', 'currency': "USD"})
            user = session.query(User).filter(User.id == id).first()
            wallets = [
                {
                    **line.wallet_object.to_dict(), 
                    'user_type': line.user_type,
                    'is_default': user.default_wallet == line.wallet if user and user.default_wallet else False
                }
                for line in session.query(User2Wallet).filter(User2Wallet.user == id)
            ]
    return wallets

def get_default_wallet_data(user_id: int):
    with Session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            add_user_data({'id': user_id})
            user = session.query(User).filter(User.id == user_id).first()

        user_wallet = None
        if user.default_wallet:
            user_wallet = (
                session.query(User2Wallet)
                .filter(User2Wallet.user == user_id, User2Wallet.wallet == user.default_wallet)
                .first()
            )

        if user_wallet is None:
            user_wallet = (
                session.query(User2Wallet)
                .filter(User2Wallet.user == user_id)
                .order_by(User2Wallet.id.asc())
                .first()
            )
            if user_wallet is None:
                add_wallet_data({'user_id': user_id, 'name': 'Personal wallet', 'currency': "USD"})
                user_wallet = (
                    session.query(User2Wallet)
                    .filter(User2Wallet.user == user_id)
                    .order_by(User2Wallet.id.asc())
                    .first()
                )
            user.default_wallet = user_wallet.wallet
            session.commit()

        return {
            **user_wallet.wallet_object.to_dict(),
            'user_type': user_wallet.user_type,
            'is_default': True,
        }

def set_default_wallet_data(user_id: int, wallet_id: int):
    with Session() as session:
        user_wallet = (
            session.query(User2Wallet)
            .filter(User2Wallet.user == user_id, User2Wallet.wallet == wallet_id)
            .first()
        )
        if user_wallet is None:
            raise ValueError('Wallet not found for user')

        user = session.query(User).filter(User.id == user_id).first()
        user.default_wallet = wallet_id
        session.commit()
        return user_wallet.wallet_object.to_dict()

def get_wallet_expense_categories_data(wallet_id: int):
    with Session() as session:
        return [
            category.to_dict()
            for category in session.query(Category)
            .filter(Category.wallet == wallet_id, Category.transaction_type == 'outcome')
            .order_by(Category.id.asc())
        ]

def add_user_data(user: dict):
    with Session() as session:
        user_id = session.query(User).filter(User.id == user.get('id')).all()
        if len(user_id) < 1:
            user_data_object = User(
                id=user.get('id'),
                username=user.get('username', ''),
                first_name=user.get('first_name', ''),
                last_name=user.get('last_name', ''),
                photo_url=user.get('photo_url', '')
                )
            session.add(user_data_object)
            session.commit()
            session.refresh(user_data_object)

            add_wallet_data({'user_id': user.get('id'), 'name': 'Personal wallet', 'currency': "USD"})
        else:
            print('user exists')

def add_category_data(category: dict):
    with Session() as session:
        category_data_object = Category(
            name=category['name'],
            wallet=category['wallet_id'],
            transaction_type=category['transaction_type'],
            icon=category['icon'],
            color=category['color'],
        )
        session.add(category_data_object)
        session.commit()
        session.refresh(category_data_object)

def delete_category_data(id: int):
    with Session() as session:
        session.query(Category).filter_by(id=id).delete()
        session.commit()

def update_category_data(id: int, category: dict):
    with Session() as session:
        category_data_object = session.query(Category).filter_by(id=id).first()
        category_data_object.name = category.get('name', None) or category_data_object.name
        category_data_object.icon = category.get('icon', None) or category_data_object.icon
        category_data_object.color = category.get('color', None) or category_data_object.color
        session.commit()
        session.refresh(category_data_object)

def add_wallet_data(wallet: dict):
    with Session() as session:
        wallet_object = Wallet(
            name=wallet['name'],
            currency=wallet['currency'],
            default_currency=wallet.get('default_currency') or wallet.get('currency') or DEFAULT_CURRENCY,
        )
        session.add(wallet_object)
        session.commit()
        session.refresh(wallet_object)


        user2wallet_data_object = User2Wallet(
            user=wallet['user_id'],
            wallet=wallet_object.id,
            user_type='owner'
        )
        session.add(user2wallet_data_object)
        session.commit()
        session.refresh(user2wallet_data_object)

        user = session.query(User).filter(User.id == wallet['user_id']).first()
        if user is not None and user.default_wallet is None:
            user.default_wallet = wallet_object.id
            session.commit()


        for category in default_categories:
            category['wallet_id'] = wallet_object.id
            add_category_data(category)

def delete_wallet_data(id: int):
    with Session() as session:
        session.query(User).filter(User.default_wallet == id).update({User.default_wallet: None})
        session.query(Transaction).filter_by(wallet=id).delete()
        session.query(Category).filter_by(wallet=id).delete()
        session.query(User2Wallet).filter_by(wallet=id).delete()
        session.query(Wallet).filter_by(id=id).delete()
        session.commit()

def update_wallet_data(id: int, wallet: dict):
    with Session() as session:
        wallet_data_object = session.query(Wallet).filter_by(id=id).first()
        wallet_data_object.name = wallet.get('name', None) or wallet_data_object.name
        wallet_data_object.default_currency = wallet.get('default_currency', None) or wallet_data_object.default_currency
        wallet_data_object.currency = wallet_data_object.default_currency
        session.commit()
        session.refresh(wallet_data_object)

def add_transaction_data(transaction: dict):
    with Session() as session:
        date = datetime.fromisoformat(transaction['date'])
        currency = transaction.get('currency')
        if not currency and transaction.get('wallet_id'):
            wallet = session.query(Wallet).filter_by(id=transaction['wallet_id']).first()
            currency = wallet.default_currency if wallet else DEFAULT_CURRENCY
        currency = (currency or DEFAULT_CURRENCY).upper()
        usd_to_currency_rate = transaction.get('usd_to_currency_rate') or get_currency_rate_data(currency, date.date())
        transaction_data_object = Transaction(
            category=transaction['category_id'],
            description=transaction['description'],
            value=transaction['value'],
            wallet=transaction['wallet_id'],
            source=transaction['source'],
            date=date,
            user=transaction['user_id'],
            currency=currency,
            usd_to_currency_rate=usd_to_currency_rate,
        )
        session.add(transaction_data_object)
        session.commit()
        session.refresh(transaction_data_object)

def delete_transaction_data(id: int):
    with Session() as session:
        session.query(Transaction).filter_by(id=id).delete()
        session.commit()

def update_transaction_data(id: int, transaction: dict):
    with Session() as session:
        transaction_data_object = session.query(Transaction).filter_by(id=id).first()
        if transaction.get('category_id', None) is not None:
            transaction_data_object.category = transaction['category_id']
        transaction_data_object.description = transaction.get('description', None) or transaction_data_object.description
        transaction_data_object.value = transaction.get('value', None) or transaction_data_object.value
        transaction_date = datetime.fromisoformat(transaction.get('date', None)) if transaction.get('date', None) else transaction_data_object.date
        transaction_data_object.date = transaction_date
        transaction_data_object.source = transaction.get('source', None) or transaction_data_object.source
        if transaction.get('currency') or transaction.get('date'):
            transaction_data_object.currency = (transaction.get('currency') or transaction_data_object.currency).upper()
            transaction_data_object.usd_to_currency_rate = get_currency_rate_data(transaction_data_object.currency, transaction_date.date())
        session.commit()
        session.refresh(transaction_data_object)

def get_wallet_users_data(id: int):
    with Session() as session:
        users_wallets = session.query(User2Wallet).filter(User2Wallet.wallet == id).all()
        result = [
            {
                **user_wallet.user_object.to_dict(), 
                'user_type': user_wallet.user_type 
            }
            for user_wallet in users_wallets
        ]
        return result 

def add_user_to_wallet(wallet_id: int,  user_id: int):
    with Session() as session:
        user_type = 'member'
        users_wallet = (
            session
            .query(User2Wallet)
            .filter_by(wallet=wallet_id, user=user_id)
            .all()
        )

        if(len(users_wallet) > 0):
            raise Exception('User already in wallet')

        user2wallet_data_object = User2Wallet(
            user=user_id, 
            wallet=wallet_id,
            user_type=user_type
        )
        session.add(user2wallet_data_object)
        session.commit()
        session.refresh(user2wallet_data_object)
