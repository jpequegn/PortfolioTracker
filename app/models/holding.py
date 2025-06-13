from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    quantity = Column(Numeric(15, 6), nullable=False, default=0)
    average_cost = Column(Numeric(10, 4), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="holdings")
    asset = relationship("Asset", back_populates="holdings")