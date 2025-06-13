from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .holding import HoldingWithAsset


class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class Portfolio(PortfolioBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PortfolioWithHoldings(Portfolio):
    holdings: List[HoldingWithAsset] = []

    class Config:
        from_attributes = True