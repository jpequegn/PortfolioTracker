from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.asset import Asset
from app.schemas.asset import AssetCreate, AssetUpdate


class CRUDAsset(CRUDBase[Asset, AssetCreate, AssetUpdate]):
    def get_by_symbol(self, db: Session, *, symbol: str) -> Optional[Asset]:
        return db.query(Asset).filter(Asset.symbol == symbol).first()

    def search_by_name_or_symbol(self, db: Session, *, query: str, limit: int = 10):
        return (
            db.query(Asset)
            .filter(
                (Asset.name.ilike(f"%{query}%")) | (Asset.symbol.ilike(f"%{query}%"))
            )
            .limit(limit)
            .all()
        )


asset = CRUDAsset(Asset)