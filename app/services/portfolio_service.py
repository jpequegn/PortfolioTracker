from typing import Dict, List
from decimal import Decimal
from sqlalchemy.orm import Session
from app.crud.portfolio import portfolio
from app.crud.holding import holding
from app.crud.transaction import transaction
from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate


class PortfolioService:
    @staticmethod
    def calculate_portfolio_value(db: Session, portfolio_id: int) -> Dict:
        """Calculate total portfolio value and performance metrics"""
        holdings = holding.get_by_portfolio(db, portfolio_id=portfolio_id)
        
        total_value = Decimal("0")
        total_cost = Decimal("0")
        asset_breakdown = []
        
        for holding_obj in holdings:
            if holding_obj.asset.current_price:
                current_value = holding_obj.quantity * holding_obj.asset.current_price
                cost_basis = holding_obj.quantity * holding_obj.average_cost
                
                gain_loss = current_value - cost_basis
                gain_loss_percent = (gain_loss / cost_basis * 100) if cost_basis > 0 else Decimal("0")
                
                asset_breakdown.append({
                    "asset": {
                        "id": holding_obj.asset.id,
                        "symbol": holding_obj.asset.symbol,
                        "name": holding_obj.asset.name,
                        "asset_type": holding_obj.asset.asset_type
                    },
                    "quantity": holding_obj.quantity,
                    "average_cost": holding_obj.average_cost,
                    "current_price": holding_obj.asset.current_price,
                    "current_value": current_value,
                    "cost_basis": cost_basis,
                    "gain_loss": gain_loss,
                    "gain_loss_percent": gain_loss_percent
                })
                
                total_value += current_value
                total_cost += cost_basis
        
        total_gain_loss = total_value - total_cost
        total_gain_loss_percent = (total_gain_loss / total_cost * 100) if total_cost > 0 else Decimal("0")
        
        return {
            "portfolio_id": portfolio_id,
            "total_value": total_value,
            "total_cost": total_cost,
            "total_gain_loss": total_gain_loss,
            "total_gain_loss_percent": total_gain_loss_percent,
            "holdings": asset_breakdown
        }

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
        """Calculate portfolio diversification by asset type and individual holdings"""
        holdings = holding.get_by_portfolio(db, portfolio_id=portfolio_id)
        
        total_value = Decimal("0")
        type_breakdown = {}
        asset_breakdown = []
        
        for holding_obj in holdings:
            if holding_obj.asset.current_price:
                current_value = holding_obj.quantity * holding_obj.asset.current_price
                total_value += current_value
                
                # Asset type breakdown
                asset_type = holding_obj.asset.asset_type.value
                if asset_type not in type_breakdown:
                    type_breakdown[asset_type] = Decimal("0")
                type_breakdown[asset_type] += current_value
                
                asset_breakdown.append({
                    "asset": {
                        "symbol": holding_obj.asset.symbol,
                        "name": holding_obj.asset.name,
                        "asset_type": asset_type
                    },
                    "value": current_value
                })
        
        # Calculate percentages
        type_percentages = {}
        for asset_type, value in type_breakdown.items():
            type_percentages[asset_type] = (value / total_value * 100) if total_value > 0 else Decimal("0")
        
        asset_percentages = []
        for asset in asset_breakdown:
            percentage = (asset["value"] / total_value * 100) if total_value > 0 else Decimal("0")
            asset_percentages.append({
                **asset,
                "percentage": percentage
            })
        
        return {
            "total_value": total_value,
            "by_asset_type": type_percentages,
            "by_asset": asset_percentages
        }