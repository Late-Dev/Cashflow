import os

import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from utils import validate_initData, create_access_token

from schema import (
        CategorySchema,
        TransactionSchema,
        TransactionUpdateSchema,
        UserSchema,
        WalletSchema,
        AuthenticationRequestSchema,
        AuthenticationResponseSchema
)
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def val_jwt(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="User not found",
            headers={"WWW-Authenticate": "Basic"},
        )
    except (jwt.InvalidTokenError, Exception) as e:
        print(e)

        raise HTTPException(
            status_code=500,
            detail="jwt error",
            headers={"WWW-Authenticate": "Basic"},
        )


SECRET_KEY = os.getenv("SECRET_KEY", None)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
    "http://127.0.0.1",
    'http://localhost:5080',
    'https://cashflow.omegasoft.keenetic.name',
    'https://tg-webapp.omegasoft.keenetic.name'
]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.middleware("https")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response



@app.options("/{path:path}")
async def options_handler(path: str):
    return {
        "allowed_methods": ["OPTIONS", "POST", "GET", "DELETE", "PATCH"]
    }


@app.get("/")
async def healthcheck():
    return "I am alive!"

@app.post("/login")
async def login(schema: AuthenticationRequestSchema) -> AuthenticationResponseSchema:
    BOT_TOKEN = os.getenv("TOKEN", None)
    is_valid = validate_initData(schema.hash_str, schema.initData, BOT_TOKEN)

    if is_valid:
        jwt_token = create_access_token(
                SECRET_KEY,
                ALGORITHM,
                ACCESS_TOKEN_EXPIRE_MINUTES,
                data={}
        )

        return {'jwt_token': jwt_token}
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
        return None

@app.get("/wallet_transactions/{id}")
def get_wallet_transactions(id: int, data = Depends(val_jwt)):
    result = get_wallet_transactions_data(id)
    return result

@app.get("/wallet_categories/{id}")
def get_wallet_categories(id: int, data = Depends(val_jwt)):
    result = get_wallet_categories_data(id)
    return result

@app.get("/user_wallets")
def get_user_wallets(data = Depends(val_jwt)):
    id = data.id
    result = get_user_wallets_data(id)
    return result

@app.post("/user")
def add_user(user: UserSchema):
    user = jsonable_encoder(user)
    add_user_data(user)
    return 'success'

@app.post("/wallet")
def add_wallet(wallet: WalletSchema, data = Depends(val_jwt)):
    wallet = jsonable_encoder(wallet)
    add_wallet_data(wallet)
    return 'success'

@app.post("/category")
def add_category(category: CategorySchema, data = Depends(val_jwt)):
    category = jsonable_encoder(category)
    add_category_data(category)
    return 'success'

@app.post("/transaction")
def add_transaction(transaction: TransactionSchema, data = Depends(val_jwt)):
    transaction = jsonable_encoder(transaction)
    add_transaction_data(transaction)
    return 'success'

@app.delete("/transaction/{id}")
def delete_transaction(id: int, data = Depends(val_jwt)):
    delete_transaction_data(id)
    return 'success'

@app.patch("/transaction/{id}")
def update_transaction(id: int, transaction: TransactionUpdateSchema, data = Depends(val_jwt)):
    transaction = jsonable_encoder(transaction)
    update_transaction_data(id, transaction)
    return 'success'
