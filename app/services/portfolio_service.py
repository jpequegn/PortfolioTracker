from typing import Dict, List
from decimal import Decimal
from sqlalchemy.orm import Session
from app.crud.portfolio import portfolio
from app.crud.holding import holding
from app.crud.transaction import transaction
from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate
from app.services.analytics_service import AnalyticsService


class PortfolioService:
    @staticmethod
    def calculate_portfolio_value(db: Session, portfolio_id: int) -> Dict:
        """
        Calculate total portfolio value and performance metrics using ibis for efficient SQL operations.
        This method now uses the AnalyticsService for database-driven calculations.
        """
        analytics = AnalyticsService()
        return analytics.get_portfolio_value_analysis(portfolio_id)

    @staticmethod
    def process_transaction(db: Session, transaction_data: TransactionCreate) -> Dict:
        """Process a transaction and update holdings accordingly"""
        # Create the transaction record
        new_transaction = transaction.create(db, obj_in=transaction_data)
        
        # Get or create holding
        existing_holding = holding.get_by_portfolio_and_asset(
            db, 
            portfolio_id=transaction_data.portfolio_id,
            asset_id=transaction_data.asset_id
        )
        
        if transaction_data.transaction_type == TransactionType.BUY:
            if existing_holding:
                # Update existing holding
                new_quantity = existing_holding.quantity + transaction_data.quantity
                new_average_cost = (
                    (existing_holding.quantity * existing_holding.average_cost) +
                    (transaction_data.quantity * transaction_data.price)
                ) / new_quantity
                
                holding.update(
                    db,
                    db_obj=existing_holding,
                    obj_in={
                        "quantity": new_quantity,
                        "average_cost": new_average_cost
                    }
                )
            else:
                # Create new holding
                from app.schemas.holding import HoldingCreate
                holding_data = HoldingCreate(
                    portfolio_id=transaction_data.portfolio_id,
                    asset_id=transaction_data.asset_id,
                    quantity=transaction_data.quantity,
                    average_cost=transaction_data.price
                )
                holding.create(db, obj_in=holding_data)
                
        elif transaction_data.transaction_type == TransactionType.SELL:
            if existing_holding and existing_holding.quantity >= transaction_data.quantity:
                new_quantity = existing_holding.quantity - transaction_data.quantity
                if new_quantity == 0:
                    # Remove holding if quantity becomes zero
                    holding.remove(db, id=existing_holding.id)
                else:
                    # Update quantity (keep same average cost)
                    holding.update(
                        db,
                        db_obj=existing_holding,
                        obj_in={"quantity": new_quantity}
                    )
            else:
                raise ValueError("Insufficient holdings to sell")
        
        return {"transaction_id": new_transaction.id, "status": "processed"}

    @staticmethod
    def get_portfolio_diversification(db: Session, portfolio_id: int) -> Dict:
        """
        Calculate portfolio diversification using ibis for efficient SQL aggregations.
        This method now uses the AnalyticsService for database-driven calculations.
        """
        analytics = AnalyticsService()
        return analytics.get_portfolio_diversification_analysis(portfolio_id)
    
    @staticmethod
    def get_portfolio_performance_metrics(db: Session, portfolio_id: int) -> Dict:
        """
        Get advanced portfolio performance metrics using ibis.
        This is a new method that provides additional analytics capabilities.
        """
        analytics = AnalyticsService()
        return analytics.get_portfolio_performance_metrics(portfolio_id)
    
    @staticmethod
    def get_asset_allocation_analysis(db: Session, portfolio_id: int) -> Dict:
        """
        Perform detailed asset allocation analysis using ibis.
        This is a new method that provides sector and geographic diversification insights.
        """
        analytics = AnalyticsService()
        return analytics.get_asset_allocation_analysis(portfolio_id)