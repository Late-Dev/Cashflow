import os
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime

from default_categories import default_categories


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

    user2_wallets = relationship("User2Wallet", back_populates="user_object")
    transactions = relationship("Transaction", back_populates="user_object")


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    currency = Column(String, nullable=False)

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


def get_wallet_transactions_data(id: int):
    with Session() as session:
        all_transactions = session.query(Transaction).filter_by(wallet=id)
        transaction_types = [
            transaction_type[0]
            for transaction_type in session.query(Category.transaction_type).filter(Category.wallet == id).distinct()
        ]

        result = {
            transaction_type: [
                transaction.to_dict()
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

def get_user_wallets_data(id: int):
    with Session() as session:
        wallets = [
            {
                **line.wallet_object.to_dict(), 
                'user_type': line.user_type
            }
            for line in session.query(User2Wallet).filter(User2Wallet.user == id)
        ]
        if(len(wallets) < 1):
            add_wallet_data({'user_id': id, 'name': 'Personal wallet', 'currency': "USD"})
            wallets = [
                {
                    **line.wallet.to_dict(), 
                    'user_type': line.user_type
                }
                for line in session.query(User2Wallet).filter(User2Wallet.user == id)
            ]
    return wallets

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
        wallet = Wallet(
            name=wallet['name'],
            currency=wallet['currency']
        )
        session.add(wallet)
        session.commit()
        session.refresh(wallet)


        user2wallet_data_object = User2Wallet(
            user=wallet['user_id'],
            wallet=wallet.id,
            user_type='owner'
        )
        session.add(user2wallet_data_object)
        session.commit()
        session.refresh(user2wallet_data_object)


        for category in default_categories:
            add_category_data(category)

def delete_wallet_data(id: int):
    with Session() as session:
        session.query(Wallet).filter_by(id=id).delete()
        session.commit()

def update_wallet_data(id: int, wallet: dict):
    with Session() as session:
        wallet_data_object = session.query(Wallet).filter_by(id=id).first()
        wallet_data_object.name = wallet.get('name', None) or wallet_data_object.name
        session.commit()
        session.refresh(wallet_data_object)

def add_transaction_data(transaction: dict):
    with Session() as session:
        date = datetime.fromisoformat(transaction['date'])
        transaction_data_object = Transaction(
            category=transaction['category_id'],
            description=transaction['description'],
            value=transaction['value'],
            wallet=transaction['wallet_id'],
            source=transaction['source'],
            date=date,
            user=transaction['user_id']
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
        transaction_data_object.date = datetime.fromisoformat(transaction.get('date', None)) or transaction_data_object.date
        transaction_data_object.source = transaction.get('source', None) or transaction_data_object.source
        session.commit()
        session.refresh(transaction_data_object)

def get_wallet_users_data(id: int):
    with Session() as session:
        users_wallet = session.query(User2Wallet).filter(User2Wallet.wallet == id).all()
        result = [
            {
                **user_wal.user_object.to_dict(), 
                'user_type': user_wal.user_type 
            }
            for user_wal in users_wallet
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
