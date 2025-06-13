#!/usr/bin/env python3
"""
Script to create sample data for the portfolio tracker
"""
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.core.database import Base
from app.crud.portfolio import portfolio
from app.crud.asset import asset
from app.schemas.portfolio import PortfolioCreate
from app.schemas.asset import AssetCreate
from app.schemas.transaction import TransactionCreate
from app.models.asset import AssetType
from app.models.transaction import TransactionType
from app.services.portfolio_service import PortfolioService

# Create all tables
Base.metadata.create_all(bind=engine)


def create_sample_data():
    db = SessionLocal()
    
    try:
        # Create sample portfolios
        portfolio1 = portfolio.create(
            db,
            obj_in=PortfolioCreate(
                name="Growth Portfolio",
                description="Long-term growth focused portfolio"
            )
        )
        
        portfolio2 = portfolio.create(
            db,
            obj_in=PortfolioCreate(
                name="Conservative Portfolio",
                description="Conservative income-focused portfolio"
            )
        )
        
        # Create sample assets
        assets_data = [
            {"symbol": "AAPL", "name": "Apple Inc.", "asset_type": AssetType.STOCK, "exchange": "NASDAQ"},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "asset_type": AssetType.STOCK, "exchange": "NASDAQ"},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "asset_type": AssetType.STOCK, "exchange": "NASDAQ"},
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "asset_type": AssetType.ETF, "exchange": "NYSE"},
            {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF", "asset_type": AssetType.ETF, "exchange": "NYSE"},
            {"symbol": "BND", "name": "Vanguard Total Bond Market ETF", "asset_type": AssetType.ETF, "exchange": "NYSE"},
            {"symbol": "CASH", "name": "Cash Holdings", "asset_type": AssetType.CASH, "currency": "USD"},
        ]
        
        created_assets = []
        for asset_data in assets_data:
            created_asset = asset.create(
                db,
                obj_in=AssetCreate(**asset_data)
            )
            created_assets.append(created_asset)
        
        # Create sample transactions for portfolio 1 (Growth Portfolio)
        transactions_p1 = [
            # AAPL purchases
            TransactionCreate(
                portfolio_id=portfolio1.id,
                asset_id=created_assets[0].id,  # AAPL
                transaction_type=TransactionType.BUY,
                quantity=Decimal("10"),
                price=Decimal("150.00"),
                total_amount=Decimal("1500.00"),
                transaction_date=datetime.now() - timedelta(days=90),
                notes="Initial AAPL purchase"
            ),
            TransactionCreate(
                portfolio_id=portfolio1.id,
                asset_id=created_assets[0].id,  # AAPL
                transaction_type=TransactionType.BUY,
                quantity=Decimal("5"),
                price=Decimal("160.00"),
                total_amount=Decimal("800.00"),
                transaction_date=datetime.now() - timedelta(days=60),
                notes="Additional AAPL purchase"
            ),
            # GOOGL purchase
            TransactionCreate(
                portfolio_id=portfolio1.id,
                asset_id=created_assets[1].id,  # GOOGL
                transaction_type=TransactionType.BUY,
                quantity=Decimal("5"),
                price=Decimal("2500.00"),
                total_amount=Decimal("12500.00"),
                transaction_date=datetime.now() - timedelta(days=75),
                notes="GOOGL investment"
            ),
            # SPY ETF
            TransactionCreate(
                portfolio_id=portfolio1.id,
                asset_id=created_assets[3].id,  # SPY
                transaction_type=TransactionType.BUY,
                quantity=Decimal("20"),
                price=Decimal("400.00"),
                total_amount=Decimal("8000.00"),
                transaction_date=datetime.now() - timedelta(days=45),
                notes="SPY ETF for diversification"
            ),
            # Cash deposit
            TransactionCreate(
                portfolio_id=portfolio1.id,
                asset_id=created_assets[6].id,  # CASH
                transaction_type=TransactionType.DEPOSIT,
                quantity=Decimal("5000"),
                price=Decimal("1.00"),
                total_amount=Decimal("5000.00"),
                transaction_date=datetime.now() - timedelta(days=100),
                notes="Initial cash deposit"
            ),
        ]
        
        # Create sample transactions for portfolio 2 (Conservative Portfolio)
        transactions_p2 = [
            # Bond ETF
            TransactionCreate(
                portfolio_id=portfolio2.id,
                asset_id=created_assets[5].id,  # BND
                transaction_type=TransactionType.BUY,
                quantity=Decimal("100"),
                price=Decimal("80.00"),
                total_amount=Decimal("8000.00"),
                transaction_date=datetime.now() - timedelta(days=80),
                notes="Bond ETF for stability"
            ),
            # VTI ETF
            TransactionCreate(
                portfolio_id=portfolio2.id,
                asset_id=created_assets[4].id,  # VTI
                transaction_type=TransactionType.BUY,
                quantity=Decimal("30"),
                price=Decimal("200.00"),
                total_amount=Decimal("6000.00"),
                transaction_date=datetime.now() - timedelta(days=70),
                notes="Total market exposure"
            ),
            # MSFT
            TransactionCreate(
                portfolio_id=portfolio2.id,
                asset_id=created_assets[2].id,  # MSFT
                transaction_type=TransactionType.BUY,
                quantity=Decimal("15"),
                price=Decimal("300.00"),
                total_amount=Decimal("4500.00"),
                transaction_date=datetime.now() - timedelta(days=50),
                notes="Blue chip stock"
            ),
            # Cash
            TransactionCreate(
                portfolio_id=portfolio2.id,
                asset_id=created_assets[6].id,  # CASH
                transaction_type=TransactionType.DEPOSIT,
                quantity=Decimal("10000"),
                price=Decimal("1.00"),
                total_amount=Decimal("10000.00"),
                transaction_date=datetime.now() - timedelta(days=90),
                notes="Conservative cash position"
            ),
        ]
        
        # Process all transactions
        all_transactions = transactions_p1 + transactions_p2
        for transaction_data in all_transactions:
            try:
                PortfolioService.process_transaction(db, transaction_data)
                print(f"Processed transaction: {transaction_data.transaction_type} {transaction_data.quantity} shares")
            except Exception as e:
                print(f"Error processing transaction: {e}")
        
        print(f"Sample data created successfully!")
        print(f"Created {len(created_assets)} assets")
        print(f"Created 2 portfolios")
        print(f"Processed {len(all_transactions)} transactions")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()