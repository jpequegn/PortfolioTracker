from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.transaction import transaction
from app.crud.portfolio import portfolio
from app.crud.asset import asset
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate, TransactionWithAsset
from app.services.portfolio_service import PortfolioService

router = APIRouter()


@router.get("/", response_model=List[TransactionWithAsset])
def read_transactions(
    portfolio_id: int = None,
    asset_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get transactions, optionally filtered by portfolio or asset"""
    if portfolio_id:
        transactions = transaction.get_by_portfolio(db, portfolio_id=portfolio_id)
    elif asset_id:
        transactions = transaction.get_by_asset(db, asset_id=asset_id)
    else:
        transactions = transaction.get_multi(db, skip=skip, limit=limit)
    return transactions


@router.post("/", response_model=Transaction)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Create a new transaction and update holdings"""
    # Verify portfolio exists
    portfolio_obj = portfolio.get(db, id=transaction_data.portfolio_id)
    if not portfolio_obj:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Verify asset exists
    asset_obj = asset.get(db, id=transaction_data.asset_id)
    if not asset_obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    try:
        result = PortfolioService.process_transaction(db, transaction_data)
        # Get the created transaction
        created_transaction = transaction.get(db, id=result["transaction_id"])
        return created_transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{transaction_id}", response_model=TransactionWithAsset)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific transaction"""
    transaction = transaction.get(db, id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.put("/{transaction_id}", response_model=Transaction)
def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Update a transaction (Note: This doesn't automatically update holdings)"""
    db_transaction = transaction.get(db, id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction.update(db=db, db_obj=db_transaction, obj_in=transaction)


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    """Delete a transaction (Note: This doesn't automatically update holdings)"""
    transaction = transaction.get(db, id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction.remove(db=db, id=transaction_id)
    return {"message": "Transaction deleted successfully"}