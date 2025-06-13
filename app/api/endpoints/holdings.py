from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.holding import holding
from app.crud.portfolio import portfolio
from app.crud.asset import asset
from app.schemas.holding import Holding, HoldingCreate, HoldingUpdate, HoldingWithAsset

router = APIRouter()


@router.get("/", response_model=List[HoldingWithAsset])
def read_holdings(
    portfolio_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get holdings, optionally filtered by portfolio"""
    if portfolio_id:
        holdings = holding.get_by_portfolio(db, portfolio_id=portfolio_id)
    else:
        holdings = holding.get_multi(db, skip=skip, limit=limit)
    return holdings


@router.post("/", response_model=Holding)
def create_holding(
    holding: HoldingCreate,
    db: Session = Depends(get_db)
):
    """Create a new holding"""
    # Verify portfolio exists
    portfolio = portfolio.get(db, id=holding.portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Verify asset exists
    asset = asset.get(db, id=holding.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Check if holding already exists
    existing_holding = holding.get_by_portfolio_and_asset(
        db, portfolio_id=holding.portfolio_id, asset_id=holding.asset_id
    )
    if existing_holding:
        raise HTTPException(
            status_code=400, 
            detail="Holding for this asset already exists in the portfolio"
        )
    
    return holding.create(db=db, obj_in=holding)


@router.get("/{holding_id}", response_model=HoldingWithAsset)
def read_holding(
    holding_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific holding"""
    holding = holding.get(db, id=holding_id)
    if holding is None:
        raise HTTPException(status_code=404, detail="Holding not found")
    return holding


@router.put("/{holding_id}", response_model=Holding)
def update_holding(
    holding_id: int,
    holding: HoldingUpdate,
    db: Session = Depends(get_db)
):
    """Update a holding"""
    db_holding = holding.get(db, id=holding_id)
    if db_holding is None:
        raise HTTPException(status_code=404, detail="Holding not found")
    return holding.update(db=db, db_obj=db_holding, obj_in=holding)


@router.delete("/{holding_id}")
def delete_holding(
    holding_id: int,
    db: Session = Depends(get_db)
):
    """Delete a holding"""
    holding = holding.get(db, id=holding_id)
    if holding is None:
        raise HTTPException(status_code=404, detail="Holding not found")
    holding.remove(db=db, id=holding_id)
    return {"message": "Holding deleted successfully"}