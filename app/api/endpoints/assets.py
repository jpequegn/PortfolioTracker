from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.asset import asset
from app.schemas.asset import Asset, AssetCreate, AssetUpdate
from app.services.price_service import PriceService

router = APIRouter()


@router.get("/", response_model=List[Asset])
def read_assets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all assets"""
    assets = asset.get_multi(db, skip=skip, limit=limit)
    return assets


@router.post("/", response_model=Asset)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db)
):
    """Create a new asset"""
    # Check if asset with symbol already exists
    existing_asset = asset.get_by_symbol(db, symbol=asset.symbol)
    if existing_asset:
        raise HTTPException(status_code=400, detail="Asset with this symbol already exists")
    
    return asset.create(db=db, obj_in=asset)


@router.get("/search")
def search_assets(
    q: str = Query(..., description="Search query for asset name or symbol"),
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Search assets by name or symbol"""
    assets = asset.search_by_name_or_symbol(db, query=q, limit=limit)
    return assets


@router.get("/lookup/{symbol}")
def lookup_asset(symbol: str):
    """Lookup asset information from external data source"""
    asset_info = PriceService.get_asset_info(symbol)
    return asset_info


@router.post("/lookup/{symbol}/create", response_model=Asset)
def create_asset_from_lookup(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Create asset from external lookup"""
    # Check if asset already exists
    existing_asset = asset.get_by_symbol(db, symbol=symbol.upper())
    if existing_asset:
        return existing_asset
    
    # Get asset info from external source
    asset_info = PriceService.get_asset_info(symbol)
    
    # Create asset
    asset_data = AssetCreate(
        symbol=asset_info['symbol'],
        name=asset_info['name'],
        asset_type=asset_info['asset_type'],
        exchange=asset_info.get('exchange'),
        currency=asset_info.get('currency', 'USD')
    )
    
    asset = asset.create(db=db, obj_in=asset_data)
    
    # Update with current price if available
    if asset_info.get('current_price'):
        asset.update(
            db,
            db_obj=asset,
            obj_in={"current_price": asset_info['current_price']}
        )
    
    return asset


@router.get("/{asset_id}", response_model=Asset)
def read_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific asset"""
    asset = asset.get(db, id=asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=Asset)
def update_asset(
    asset_id: int,
    asset: AssetUpdate,
    db: Session = Depends(get_db)
):
    """Update an asset"""
    db_asset = asset.get(db, id=asset_id)
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset.update(db=db, db_obj=db_asset, obj_in=asset)


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    """Delete an asset"""
    asset = asset.get(db, id=asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset.remove(db=db, id=asset_id)
    return {"message": "Asset deleted successfully"}


@router.post("/update-prices")
def update_asset_prices(
    asset_ids: List[int] = None,
    db: Session = Depends(get_db)
):
    """Update current prices for assets"""
    PriceService.update_asset_prices(db, asset_ids)
    return {"message": "Asset prices updated successfully"}