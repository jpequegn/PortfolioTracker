from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.holding import Holding
from app.schemas.holding import HoldingCreate, HoldingUpdate


class CRUDHolding(CRUDBase[Holding, HoldingCreate, HoldingUpdate]):
    def get_by_portfolio(self, db: Session, *, portfolio_id: int) -> List[Holding]:
        return (
            db.query(Holding)
            .options(joinedload(Holding.asset))
            .filter(Holding.portfolio_id == portfolio_id)
            .all()
        )

    def get_by_portfolio_and_asset(
        self, db: Session, *, portfolio_id: int, asset_id: int
    ) -> Optional[Holding]:
        return (
            db.query(Holding)
            .filter(
                Holding.portfolio_id == portfolio_id,
                Holding.asset_id == asset_id
            )
            .first()
        )


holding = CRUDHolding(Holding)