from typing import List
from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


class CRUDTransaction(CRUDBase[Transaction, TransactionCreate, TransactionUpdate]):
    def get_by_portfolio(self, db: Session, *, portfolio_id: int) -> List[Transaction]:
        return (
            db.query(Transaction)
            .options(joinedload(Transaction.asset))
            .filter(Transaction.portfolio_id == portfolio_id)
            .order_by(Transaction.transaction_date.desc())
            .all()
        )

    def get_by_asset(self, db: Session, *, asset_id: int) -> List[Transaction]:
        return (
            db.query(Transaction)
            .options(joinedload(Transaction.asset))
            .filter(Transaction.asset_id == asset_id)
            .order_by(Transaction.transaction_date.desc())
            .all()
        )


transaction = CRUDTransaction(Transaction)