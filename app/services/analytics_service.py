import ibis
from typing import Dict, List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from app.core.database import get_db_url


class AnalyticsService:
    """
    Analytics service using Ibis for efficient database-driven analytics.
    This replaces manual Python calculations with SQL-based operations.
    """
    
    def __init__(self):
        # Connect to the same SQLite database using ibis
        db_url = get_db_url()
        # Convert SQLAlchemy URL to ibis format
        if db_url.startswith("sqlite:///"):
            db_path = db_url.replace("sqlite:///", "")
            self.con = ibis.sqlite.connect(db_path)
        else:
            raise ValueError(f"Unsupported database URL: {db_url}")
    
    def get_portfolio_value_analysis(self, portfolio_id: int) -> Dict:
        """
        Calculate portfolio value and performance using ibis for efficient SQL operations.
        This replaces the manual calculations in PortfolioService.calculate_portfolio_value.
        """
        # Define tables
        holdings = self.con.table("holdings")
        assets = self.con.table("assets")
        
        # Join holdings with assets and calculate metrics
        portfolio_data = (
            holdings
            .join(assets, holdings.asset_id == assets.id)
            .filter(holdings.portfolio_id == portfolio_id)
            .filter(assets.current_price.notnull())
            .select([
                holdings.id.name("holding_id"),
                assets.id.name("asset_id"),
                assets.symbol,
                assets.name.name("asset_name"),
                assets.asset_type,
                assets.current_price,
                holdings.quantity,
                holdings.average_cost,
                (holdings.quantity * assets.current_price).name("current_value"),
                (holdings.quantity * holdings.average_cost).name("cost_basis"),
                ((holdings.quantity * assets.current_price) - (holdings.quantity * holdings.average_cost)).name("gain_loss"),
                (
                    ((holdings.quantity * assets.current_price) - (holdings.quantity * holdings.average_cost)) 
                    / (holdings.quantity * holdings.average_cost) * 100
                ).name("gain_loss_percent")
            ])
        )
        
        # Execute query and get results
        results = portfolio_data.execute()
        
        if results.empty:
            return {
                "portfolio_id": portfolio_id,
                "total_value": Decimal("0"),
                "total_cost": Decimal("0"),
                "total_gain_loss": Decimal("0"),
                "total_gain_loss_percent": Decimal("0"),
                "holdings": []
            }
        
        # Calculate totals
        total_value = Decimal(str(results["current_value"].sum()))
        total_cost = Decimal(str(results["cost_basis"].sum()))
        total_gain_loss = total_value - total_cost
        total_gain_loss_percent = (total_gain_loss / total_cost * 100) if total_cost > 0 else Decimal("0")
        
        # Format holdings data
        holdings_data = []
        for _, row in results.iterrows():
            holdings_data.append({
                "asset": {
                    "id": int(row["asset_id"]),
                    "symbol": row["symbol"],
                    "name": row["asset_name"],
                    "asset_type": row["asset_type"]
                },
                "quantity": Decimal(str(row["quantity"])),
                "average_cost": Decimal(str(row["average_cost"])),
                "current_price": Decimal(str(row["current_price"])),
                "current_value": Decimal(str(row["current_value"])),
                "cost_basis": Decimal(str(row["cost_basis"])),
                "gain_loss": Decimal(str(row["gain_loss"])),
                "gain_loss_percent": Decimal(str(row["gain_loss_percent"]))
            })
        
        return {
            "portfolio_id": portfolio_id,
            "total_value": total_value,
            "total_cost": total_cost,
            "total_gain_loss": total_gain_loss,
            "total_gain_loss_percent": total_gain_loss_percent,
            "holdings": holdings_data
        }
    
    def get_portfolio_diversification_analysis(self, portfolio_id: int) -> Dict:
        """
        Calculate portfolio diversification using ibis aggregations.
        This replaces the manual calculations in PortfolioService.get_portfolio_diversification.
        """
        # Define tables
        holdings = self.con.table("holdings")
        assets = self.con.table("assets")
        
        # Get portfolio holdings with current values
        portfolio_holdings = (
            holdings
            .join(assets, holdings.asset_id == assets.id)
            .filter(holdings.portfolio_id == portfolio_id)
            .filter(assets.current_price.notnull())
            .select([
                assets.symbol,
                assets.name.name("asset_name"),
                assets.asset_type,
                (holdings.quantity * assets.current_price).name("current_value")
            ])
        )
        
        # Calculate total portfolio value
        total_value_query = portfolio_holdings.aggregate(
            total_value=portfolio_holdings.current_value.sum()
        )
        total_value_result = total_value_query.execute()
        total_value = Decimal(str(total_value_result["total_value"].iloc[0])) if not total_value_result.empty else Decimal("0")
        
        if total_value == 0:
            return {
                "total_value": total_value,
                "by_asset_type": {},
                "by_asset": []
            }
        
        # Calculate breakdown by asset type
        type_breakdown_query = (
            portfolio_holdings
            .group_by("asset_type")
            .aggregate(type_value=portfolio_holdings.current_value.sum())
        )
        type_breakdown_results = type_breakdown_query.execute()
        
        type_percentages = {}
        for _, row in type_breakdown_results.iterrows():
            asset_type = row["asset_type"]
            type_value = Decimal(str(row["type_value"]))
            percentage = (type_value / total_value * 100) if total_value > 0 else Decimal("0")
            type_percentages[asset_type] = percentage
        
        # Get individual asset breakdown
        asset_breakdown_results = portfolio_holdings.execute()
        asset_percentages = []
        for _, row in asset_breakdown_results.iterrows():
            current_value = Decimal(str(row["current_value"]))
            percentage = (current_value / total_value * 100) if total_value > 0 else Decimal("0")
            asset_percentages.append({
                "asset": {
                    "symbol": row["symbol"],
                    "name": row["asset_name"],
                    "asset_type": row["asset_type"]
                },
                "value": current_value,
                "percentage": percentage
            })
        
        return {
            "total_value": total_value,
            "by_asset_type": type_percentages,
            "by_asset": asset_percentages
        }
    
    def get_portfolio_performance_metrics(self, portfolio_id: int) -> Dict:
        """
        Calculate advanced portfolio performance metrics using ibis.
        This provides additional analytics not available in the original service.
        """
        # Define tables
        holdings = self.con.table("holdings")
        assets = self.con.table("assets")
        transactions = self.con.table("transactions")
        
        # Get portfolio performance data
        performance_query = (
            holdings
            .join(assets, holdings.asset_id == assets.id)
            .filter(holdings.portfolio_id == portfolio_id)
            .filter(assets.current_price.notnull())
            .aggregate([
                holdings.quantity.sum().name("total_shares"),
                (holdings.quantity * assets.current_price).sum().name("total_market_value"),
                (holdings.quantity * holdings.average_cost).sum().name("total_cost_basis"),
                assets.current_price.max().name("max_price"),
                assets.current_price.min().name("min_price"),
                assets.current_price.mean().name("avg_price")
            ])
        )
        
        performance_result = performance_query.execute()
        
        if performance_result.empty:
            return {
                "portfolio_id": portfolio_id,
                "total_positions": 0,
                "total_market_value": Decimal("0"),
                "total_cost_basis": Decimal("0"),
                "unrealized_gain_loss": Decimal("0"),
                "unrealized_gain_loss_percent": Decimal("0"),
                "price_statistics": {
                    "max_price": Decimal("0"),
                    "min_price": Decimal("0"),
                    "avg_price": Decimal("0")
                }
            }
        
        row = performance_result.iloc[0]
        total_market_value = Decimal(str(row["total_market_value"]))
        total_cost_basis = Decimal(str(row["total_cost_basis"]))
        unrealized_gain_loss = total_market_value - total_cost_basis
        unrealized_gain_loss_percent = (unrealized_gain_loss / total_cost_basis * 100) if total_cost_basis > 0 else Decimal("0")
        
        # Count total positions
        positions_query = (
            holdings
            .filter(holdings.portfolio_id == portfolio_id)
            .aggregate(total_positions=holdings.id.count())
        )
        positions_result = positions_query.execute()
        total_positions = int(positions_result["total_positions"].iloc[0]) if not positions_result.empty else 0
        
        return {
            "portfolio_id": portfolio_id,
            "total_positions": total_positions,
            "total_market_value": total_market_value,
            "total_cost_basis": total_cost_basis,
            "unrealized_gain_loss": unrealized_gain_loss,
            "unrealized_gain_loss_percent": unrealized_gain_loss_percent,
            "price_statistics": {
                "max_price": Decimal(str(row["max_price"])),
                "min_price": Decimal(str(row["min_price"])),
                "avg_price": Decimal(str(row["avg_price"]))
            }
        }
    
    def get_asset_allocation_analysis(self, portfolio_id: int) -> Dict:
        """
        Perform detailed asset allocation analysis using ibis.
        This provides asset type and currency diversification insights.
        """
        # Define tables
        holdings = self.con.table("holdings")
        assets = self.con.table("assets")
        
        # Get asset allocation data (only using columns that exist)
        allocation_query = (
            holdings
            .join(assets, holdings.asset_id == assets.id)
            .filter(holdings.portfolio_id == portfolio_id)
            .filter(assets.current_price.notnull())
            .select([
                assets.asset_type,
                assets.currency,
                (holdings.quantity * assets.current_price).name("market_value")
            ])
        )
        
        allocation_results = allocation_query.execute()
        
        if allocation_results.empty:
            return {
                "portfolio_id": portfolio_id,
                "by_asset_type": {},
                "by_currency": {},
                "total_value": Decimal("0")
            }
        
        total_value = Decimal(str(allocation_results["market_value"].sum()))
        
        # Calculate allocation by asset type
        by_asset_type = {}
        asset_type_groups = allocation_results.groupby("asset_type")["market_value"].sum()
        for asset_type, value in asset_type_groups.items():
            percentage = (Decimal(str(value)) / total_value * 100) if total_value > 0 else Decimal("0")
            by_asset_type[asset_type] = {
                "value": Decimal(str(value)),
                "percentage": percentage
            }
        
        # Calculate allocation by currency
        by_currency = {}
        currency_groups = allocation_results.groupby("currency")["market_value"].sum()
        for currency, value in currency_groups.items():
            percentage = (Decimal(str(value)) / total_value * 100) if total_value > 0 else Decimal("0")
            by_currency[currency] = {
                "value": Decimal(str(value)),
                "percentage": percentage
            }
        
        return {
            "portfolio_id": portfolio_id,
            "by_asset_type": by_asset_type,
            "by_currency": by_currency,
            "total_value": total_value
        }