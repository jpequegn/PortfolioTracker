from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from .asset import Asset


class HoldingBase(BaseModel):
    portfolio_id: int
    asset_id: int
    quantity: Decimal
    average_cost: Decimal


class HoldingCreate(HoldingBase):
    pass


class HoldingUpdate(BaseModel):
    quantity: Optional[Decimal] = None
    average_cost: Optional[Decimal] = None


class Holding(HoldingBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HoldingWithAsset(Holding):
    asset: Asset

    class Config:
        from_attributes = True