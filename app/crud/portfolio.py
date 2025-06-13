from typing import List
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.portfolio import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioUpdate


class CRUDPortfolio(CRUDBase[Portfolio, PortfolioCreate, PortfolioUpdate]):
    def get_with_holdings(self, db: Session, *, id: int) -> Portfolio:
        return (
            db.query(Portfolio)
            .options(joinedload(Portfolio.holdings).joinedload("asset"))
            .filter(Portfolio.id == id)
            .first()
        )

    def get_multi_with_holdings(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Portfolio]:
        return (
            db.query(Portfolio)
            .options(joinedload(Portfolio.holdings).joinedload("asset"))
            .offset(skip)
            .limit(limit)
            .all()
        )


portfolio = CRUDPortfolio(Portfolio)