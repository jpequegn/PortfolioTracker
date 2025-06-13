from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.portfolio import portfolio
from app.schemas.portfolio import Portfolio, PortfolioCreate, PortfolioUpdate, PortfolioWithHoldings
from app.services.portfolio_service import PortfolioService
from app.services.price_service import PriceService

router = APIRouter()


@router.get("/", response_model=List[Portfolio])
def read_portfolios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all portfolios"""
    portfolios = portfolio.get_multi(db, skip=skip, limit=limit)
    return portfolios


@router.post("/", response_model=Portfolio)
def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: Session = Depends(get_db)
):
    """Create a new portfolio"""
    return portfolio.create(db=db, obj_in=portfolio_data)


@router.get("/{portfolio_id}", response_model=PortfolioWithHoldings)
def read_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific portfolio with holdings"""
    portfolio_obj = portfolio.get_with_holdings(db, id=portfolio_id)
    if portfolio_obj is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio_obj


@router.put("/{portfolio_id}", response_model=Portfolio)
def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,
    db: Session = Depends(get_db)
):
    """Update a portfolio"""
    db_portfolio = portfolio.get(db, id=portfolio_id)
    if db_portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio.update(db=db, db_obj=db_portfolio, obj_in=portfolio_update)


@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Delete a portfolio"""
    portfolio_obj = portfolio.get(db, id=portfolio_id)
    if portfolio_obj is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    portfolio.remove(db=db, id=portfolio_id)
    return {"message": "Portfolio deleted successfully"}


@router.get("/{portfolio_id}/performance")
def get_portfolio_performance(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get portfolio performance metrics"""
    portfolio_obj = portfolio.get(db, id=portfolio_id)
    if portfolio_obj is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Update prices before calculating performance
    PriceService.update_asset_prices(db)
    
    return PortfolioService.calculate_portfolio_value(db, portfolio_id)


@router.get("/{portfolio_id}/diversification")
def get_portfolio_diversification(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get portfolio diversification analysis"""
    portfolio_obj = portfolio.get(db, id=portfolio_id)
    if portfolio_obj is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    return PortfolioService.get_portfolio_diversification(db, portfolio_id)