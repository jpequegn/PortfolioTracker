from sqlalchemy import Column, Integer, String, Enum, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class AssetType(str, enum.Enum):
    STOCK = "stock"
    BOND = "bond"
    ETF = "etf"
    CASH = "cash"
    CRYPTO = "crypto"
    COMMODITY = "commodity"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    asset_type = Column(Enum(AssetType), nullable=False)
    exchange = Column(String(50), nullable=True)
    currency = Column(String(3), default="USD")
    current_price = Column(Numeric(10, 4), nullable=True)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    holdings = relationship("Holding", back_populates="asset")
    transactions = relationship("Transaction", back_populates="asset")