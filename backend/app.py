import os

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from schema import CategorySchema, TransactionSchema, TransactionUpdateSchema, UserSchema, WalletSchema
from database import (
    add_category_data, 
    add_transaction_data, 
    add_user_data, 
    add_wallet_data, 
    db,
    delete_transaction_data,
    get_user_wallets_data,
    get_wallet_categories_data, 
    get_wallet_transactions_data,
    update_transaction_data
)


app = FastAPI()

db.bind(
    provider='postgres', 
    user=os.environ['POSTGRES_USER'], 
    password=os.environ['POSTGRES_PASSWORD'], 
    host='db',
    database='cashflow'
)
db.generate_mapping(create_tables=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
    "http://127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def healthcheck():
    return "I am alive!"

@app.get("/wallet_transactions/{id}")
def get_wallet_transactions(id: int):
    result = get_wallet_transactions_data(id)
    return result

@app.get("/wallet_categories/{id}")
def get_wallet_categories(id: int):
    result = get_wallet_categories_data(id)
    return result

@app.get("/user_wallets/{id}")
def get_user_wallets(id: int):
    result = get_user_wallets_data(id)
    return result

@app.post("/user")
def add_user(user: UserSchema):
    user = jsonable_encoder(user)
    add_user_data(user)
    return 'success'

@app.post("/wallet")
def add_wallet(wallet: WalletSchema):
    wallet = jsonable_encoder(wallet)
    add_wallet_data(wallet)
    return 'success'

@app.post("/category")
def add_category(category: CategorySchema):
    category = jsonable_encoder(category)
    add_category_data(category)
    return 'success'

@app.post("/transaction")
def add_transaction(transaction: TransactionSchema):
    transaction = jsonable_encoder(transaction)
    add_transaction_data(transaction)
    return 'success'

@app.delete("/transaction/{id}")
def delete_transaction(id: int):
    delete_transaction_data(id)
    return 'success'

@app.patch("/transaction/{id}")
def update_transaction(id: int, transaction: TransactionUpdateSchema):
    transaction = jsonable_encoder(transaction)
    update_transaction_data(id, transaction)
    return 'success'
