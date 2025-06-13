from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    holdings = relationship("Holding", back_populates="portfolio", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")