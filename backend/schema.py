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
    name: str
    currency: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Family finances",
                "currency": "dollar"
            }
        }

class CategorySchema(BaseModel):
    name: str
    wallet_id: int
    transaction_type: str
    icon: str
    color: int

    class Config:
        schema_extra = {
            "example": {
                "name": "education",
                "wallet_id": 0,
                "transaction_type_id": "income",
                "icon": '💵',
                "color": 45
            }
        }

class TransactionSchema(BaseModel):
    description: str
    value: Decimal
    date: datetime
    source: Optional[str]
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
                "wallet_id": 0,
            }
        }

class TransactionUpdateSchema(BaseModel):
    description: Optional[str] = None
    value: Optional[Decimal] = None
    date: Optional[datetime] = None
    source: Optional[str] = None
    category_id: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "description": "Buy beer",
                "value": Decimal("50.1"),
                "date": "2023-10-07T11:24:11.022Z",
                "source": "Amazon",
                "category_id": 0
            }
        }


class CategoryUpdateSchema(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "education",
                "icon": '💵',
                "color": 45
            }
        }


class WalletUpdateSchema(BaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Family finances"
            }
        }


class AuthenticationRequestSchema(BaseModel):
    hash_str: str
    initData: str


class AuthenticationResponseSchema(BaseModel):
    jwt_token: str

