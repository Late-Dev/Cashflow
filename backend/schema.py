from decimal import Decimal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "id": 123
            }
        }

class WalletSchema(BaseModel):
    user_id: int
    name: str
    currency: str

    class Config:
        schema_extra = {
            "example": {
                "user_id": 123,
                "name": "Family finances",
                "currency": "dollar"
            }
        }

class CategorySchema(BaseModel):
    name: str
    wallet_id: int
    transaction_type: str

    class Config:
        schema_extra = {
            "example": {
                "name": "education",
                "wallet_id": 0,
                "transaction_type_id": "income"
            }
        }

class TransactionSchema(BaseModel):
    description: str
    value: Decimal
    date: datetime
    source: str
    category_id: int
    wallet_id: int

    class Config:
        schema_extra = {
            "example": {
                "description": "Buy beer",
                "value": Decimal("50.1"),
                "date": "2023-10-07T11:24:11.022Z",
                "source": "Amazon",
                "category_id": 0,
                "wallet_id": 0
            }
        }