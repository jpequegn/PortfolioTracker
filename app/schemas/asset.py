from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.asset import AssetType


class AssetBase(BaseModel):
    symbol: str
    name: str
    asset_type: AssetType
    exchange: Optional[str] = None
    currency: str = "USD"


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    symbol: Optional[str] = None
    name: Optional[str] = None
    asset_type: Optional[AssetType] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    current_price: Optional[Decimal] = None


class Asset(AssetBase):
    id: int
    current_price: Optional[Decimal] = None
    last_updated: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True