from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.transaction import TransactionType
from .asset import Asset


class TransactionBase(BaseModel):
    portfolio_id: int
    asset_id: int
    transaction_type: TransactionType
    quantity: Decimal
    price: Decimal
    fees: Decimal = Decimal("0")
    total_amount: Decimal
    transaction_date: datetime
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    transaction_type: Optional[TransactionType] = None
    quantity: Optional[Decimal] = None
    price: Optional[Decimal] = None
    fees: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    transaction_date: Optional[datetime] = None
    notes: Optional[str] = None


class Transaction(TransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionWithAsset(Transaction):
    asset: Asset

    class Config:
        from_attributes = True