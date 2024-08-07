import os

import jwt
from fastapi import FastAPI, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from utils import validate_initData, create_access_token

from schema import (
        CategorySchema,
        CategoryUpdateSchema,
        TransactionSchema,
        TransactionUpdateSchema,
        UserSchema,
        WalletSchema,
        AuthenticationRequestSchema,
        AuthenticationResponseSchema,
        WalletUpdateSchema,
        VerificationLinkSchema
)
from database import (
    add_category_data,
    add_transaction_data,
    add_user_data,
    add_wallet_data,
    delete_category_data,
    delete_transaction_data,
    delete_wallet_data,
    get_user_wallets_data,
    get_wallet_categories_data,
    get_wallet_transactions_data,
    update_category_data,
    update_transaction_data,
    update_wallet_data,
    get_wallet_users_data,
    add_user_to_wallet
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
    is_valid, user = validate_initData(schema.hash_str, schema.initData, BOT_TOKEN)

    if is_valid:
        jwt_token = create_access_token(
                SECRET_KEY,
                ALGORITHM,
                ACCESS_TOKEN_EXPIRE_MINUTES,
                data={ 'id': user.get('id') }
        )

        add_user_data(user)

        return {'jwt_token': jwt_token}
    else:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.get("/wallet_transactions/{id}")
def get_wallet_transactions(id: int, data = Depends(val_jwt)):
    result = get_wallet_transactions_data(id)
    return result

@app.get("/wallet_users/{id}")
def get_wallet_users(id: int, data = Depends(val_jwt)):
    result = get_wallet_users_data(id)
    return result

@app.get("/wallet_categories/{id}")
def get_wallet_categories(id: int, data = Depends(val_jwt)):
    result = get_wallet_categories_data(id)
    return result

@app.get("/user_wallets")
def get_user_wallets(data = Depends(val_jwt)):
    id = data.get('id')
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
    id = data.get('id')
    wallet['user_id'] = id
    add_wallet_data(wallet)
    return 'success'

@app.delete("/wallet/{id}")
def delete_wallet(id: int, data = Depends(val_jwt)):
    delete_wallet_data(id)
    return 'success'

@app.patch("/wallet/{id}")
def update_wallet(id: int, wallet: WalletUpdateSchema, data = Depends(val_jwt)):
    wallet = jsonable_encoder(wallet)
    update_wallet_data(id, wallet)
    return 'success'

@app.post("/category")
def add_category(category: CategorySchema, data = Depends(val_jwt)):
    category = jsonable_encoder(category)
    add_category_data(category)
    return 'success'

@app.delete("/category/{id}")
def delete_category(id: int, data = Depends(val_jwt)):
    delete_category_data(id)
    return 'success'

@app.patch("/category/{id}")
def update_category(id: int, category: CategoryUpdateSchema, data = Depends(val_jwt)):
    category = jsonable_encoder(category)
    update_category_data(id, category)
    return 'success'

@app.post("/transaction")
def add_transaction(transaction: TransactionSchema, data = Depends(val_jwt)):
    transaction = jsonable_encoder(transaction)
    id = data.get('id')
    transaction['user_id'] = id
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

@app.get("/wallet_generate_link/{id}")
def wallet_generate_link(id: int, data = Depends(val_jwt)):
  token = create_access_token(
                SECRET_KEY,
                ALGORITHM,
                ACCESS_TOKEN_EXPIRE_MINUTES,
                data={ 'id': id }
        )
  return token

@app.post("/wallet_verify_link")
def wallet_verify_link(schema: VerificationLinkSchema, data = Depends(val_jwt)):
  try:
    wallet_data = jwt.decode(schema.link, SECRET_KEY, algorithms=[ALGORITHM])

    add_user_to_wallet(wallet_data.get('id'), data.get('id'))

    return 'success'
  
  except jwt.ExpiredSignatureError:
    raise HTTPException(
        status_code=401,
        detail="Link is expired",
    )

  except jwt.InvalidTokenError:
    print(schema)
    raise HTTPException(
        status_code=401,
        detail="Link is invalid",
    )

  except Exception as e:
    print(schema)
    print(e)
    raise HTTPException(
        status_code=401,
        detail=str(e),
    )


@app.get('/bot_user_wallets/{id}')
def get_bot_user_wallets(id: int, secret: str):
    if(secret == os.getenv("BOT_SECRET", None)):


        result = [ {
            **wallet,
            "link":create_access_token(
                SECRET_KEY,
                ALGORITHM,
                ACCESS_TOKEN_EXPIRE_MINUTES,
                data={ 'id': wallet.get('id') }
                ).replace(".", "__")
        } for wallet in get_user_wallets_data(id)]
        return result
    else:
        raise HTTPException(
            status_code=403,
            detail="You are not the bot",
        )
