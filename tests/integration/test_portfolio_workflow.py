"""
Integration tests for complete portfolio workflows
"""
import pytest
from fastapi import status
from decimal import Decimal


class TestPortfolioWorkflow:
    """Test complete portfolio management workflows"""

    def test_complete_portfolio_lifecycle(self, client):
        """Test a complete portfolio lifecycle from creation to performance analysis"""
        
        # 1. Create a portfolio
        portfolio_data = {
            "name": "Integration Test Portfolio",
            "description": "A portfolio for integration testing"
        }
        portfolio_response = client.post("/api/v1/portfolios/", json=portfolio_data)
        assert portfolio_response.status_code == status.HTTP_200_OK
        portfolio_id = portfolio_response.json()["id"]
        
        # 2. Create assets
        assets_data = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "asset_type": "stock",
                "exchange": "NASDAQ",
                "currency": "USD",
                "current_price": "150.00"
            },
            {
                "symbol": "GOOGL",
                "name": "Alphabet Inc.",
                "asset_type": "stock",
                "exchange": "NASDAQ",
                "currency": "USD",
                "current_price": "2500.00"
            },
            {
                "symbol": "CASH",
                "name": "US Dollar Cash",
                "asset_type": "cash",
                "exchange": "N/A",
                "currency": "USD",
                "current_price": "1.00"
            }
        ]
        
        asset_ids = []
        for asset_data in assets_data:
            asset_response = client.post("/api/v1/assets/", json=asset_data)
            assert asset_response.status_code == status.HTTP_200_OK
            asset_ids.append(asset_response.json()["id"])
        
        # 3. Create transactions
        transactions_data = [
            {
                "portfolio_id": portfolio_id,
                "asset_id": asset_ids[0],  # AAPL
                "transaction_type": "buy",
                "quantity": "10.0",
                "price": "150.00",
                "total_amount": "1500.00",
                "transaction_date": "2024-01-15T10:00:00",
                "notes": "Initial AAPL purchase"
            },
            {
                "portfolio_id": portfolio_id,
                "asset_id": asset_ids[1],  # GOOGL
                "transaction_type": "buy",
                "quantity": "2.0",
                "price": "2500.00",
                "total_amount": "5000.00",
                "transaction_date": "2024-01-16T10:00:00",
                "notes": "Initial GOOGL purchase"
            },
            {
                "portfolio_id": portfolio_id,
                "asset_id": asset_ids[2],  # CASH
                "transaction_type": "deposit",
                "quantity": "1000.0",
                "price": "1.00",
                "total_amount": "1000.00",
                "transaction_date": "2024-01-17T10:00:00",
                "notes": "Cash deposit"
            }
        ]
        
        for transaction_data in transactions_data:
            transaction_response = client.post("/api/v1/transactions/", json=transaction_data)
            assert transaction_response.status_code == status.HTTP_200_OK
        
        # 4. Verify holdings were created
        holdings_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio_id}")
        assert holdings_response.status_code == status.HTTP_200_OK
        holdings = holdings_response.json()
        assert len(holdings) == 3
        
        # 5. Check portfolio performance
        performance_response = client.get(f"/api/v1/portfolios/{portfolio_id}/performance")
        assert performance_response.status_code == status.HTTP_200_OK
        performance = performance_response.json()
        
        # Total value should be: (10 * 150) + (2 * 2500) + (1000 * 1) = 7500
        assert performance["total_value"] == 7500.0
        assert performance["total_cost_basis"] == 7500.0
        assert performance["total_gain_loss"] == 0.0
        
        # 6. Check diversification
        diversification_response = client.get(f"/api/v1/portfolios/{portfolio_id}/diversification")
        assert diversification_response.status_code == status.HTTP_200_OK
        diversification = diversification_response.json()
        
        assert "by_asset_type" in diversification
        assert "by_holding" in diversification
        
        # Should have stock and cash allocations
        asset_types = {item["asset_type"] for item in diversification["by_asset_type"]}
        assert "stock" in asset_types
        assert "cash" in asset_types

    def test_transaction_updates_holdings(self, client):
        """Test that multiple transactions correctly update holdings"""
        
        # Create portfolio and asset
        portfolio_data = {"name": "Transaction Test Portfolio"}
        portfolio_response = client.post("/api/v1/portfolios/", json=portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_data = {
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "asset_type": "stock",
            "exchange": "NASDAQ",
            "currency": "USD",
            "current_price": "200.00"
        }
        asset_response = client.post("/api/v1/assets/", json=asset_data)
        asset_id = asset_response.json()["id"]
        
        # First buy transaction
        transaction1 = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "transaction_type": "buy",
            "quantity": "5.0",
            "price": "200.00",
            "total_amount": "1000.00",
            "transaction_date": "2024-01-15T10:00:00"
        }
        client.post("/api/v1/transactions/", json=transaction1)
        
        # Check holding after first transaction
        holdings_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio_id}")
        holdings = holdings_response.json()
        assert len(holdings) == 1
        assert holdings[0]["quantity"] == "5.0"
        assert holdings[0]["average_cost"] == "200.00"
        
        # Second buy transaction at different price
        transaction2 = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "transaction_type": "buy",
            "quantity": "5.0",
            "price": "250.00",
            "total_amount": "1250.00",
            "transaction_date": "2024-01-16T10:00:00"
        }
        client.post("/api/v1/transactions/", json=transaction2)
        
        # Check holding after second transaction
        holdings_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio_id}")
        holdings = holdings_response.json()
        assert len(holdings) == 1
        assert holdings[0]["quantity"] == "10.0"
        # Average cost should be (1000 + 1250) / 10 = 225.00
        assert holdings[0]["average_cost"] == "225.00"
        
        # Sell transaction
        transaction3 = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "transaction_type": "sell",
            "quantity": "3.0",
            "price": "300.00",
            "total_amount": "900.00",
            "transaction_date": "2024-01-17T10:00:00"
        }
        client.post("/api/v1/transactions/", json=transaction3)
        
        # Check holding after sell transaction
        holdings_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio_id}")
        holdings = holdings_response.json()
        assert len(holdings) == 1
        assert holdings[0]["quantity"] == "7.0"
        # Average cost should remain the same
        assert holdings[0]["average_cost"] == "225.00"

    def test_portfolio_with_price_changes(self, client):
        """Test portfolio performance with price changes"""
        
        # Create portfolio and asset
        portfolio_data = {"name": "Price Change Test Portfolio"}
        portfolio_response = client.post("/api/v1/portfolios/", json=portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_data = {
            "symbol": "NVDA",
            "name": "NVIDIA Corporation",
            "asset_type": "stock",
            "exchange": "NASDAQ",
            "currency": "USD",
            "current_price": "100.00"
        }
        asset_response = client.post("/api/v1/assets/", json=asset_data)
        asset_id = asset_response.json()["id"]
        
        # Buy transaction
        transaction_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "transaction_type": "buy",
            "quantity": "10.0",
            "price": "100.00",
            "total_amount": "1000.00",
            "transaction_date": "2024-01-15T10:00:00"
        }
        client.post("/api/v1/transactions/", json=transaction_data)
        
        # Check initial performance
        performance_response = client.get(f"/api/v1/portfolios/{portfolio_id}/performance")
        performance = performance_response.json()
        assert performance["total_value"] == 1000.0
        assert performance["total_cost_basis"] == 1000.0
        assert performance["total_gain_loss"] == 0.0
        
        # Update asset price
        updated_asset_data = {
            **asset_data,
            "current_price": "150.00"
        }
        client.put(f"/api/v1/assets/{asset_id}", json=updated_asset_data)
        
        # Check performance after price increase
        performance_response = client.get(f"/api/v1/portfolios/{portfolio_id}/performance")
        performance = performance_response.json()
        assert performance["total_value"] == 1500.0  # 10 * 150
        assert performance["total_cost_basis"] == 1000.0
        assert performance["total_gain_loss"] == 500.0
        assert performance["total_gain_loss_percentage"] == 50.0

    def test_multiple_portfolios_isolation(self, client):
        """Test that multiple portfolios are properly isolated"""
        
        # Create two portfolios
        portfolio1_data = {"name": "Portfolio 1"}
        portfolio2_data = {"name": "Portfolio 2"}
        
        portfolio1_response = client.post("/api/v1/portfolios/", json=portfolio1_data)
        portfolio2_response = client.post("/api/v1/portfolios/", json=portfolio2_data)
        
        portfolio1_id = portfolio1_response.json()["id"]
        portfolio2_id = portfolio2_response.json()["id"]
        
        # Create asset
        asset_data = {
            "symbol": "AMD",
            "name": "Advanced Micro Devices",
            "asset_type": "stock",
            "exchange": "NASDAQ",
            "currency": "USD",
            "current_price": "80.00"
        }
        asset_response = client.post("/api/v1/assets/", json=asset_data)
        asset_id = asset_response.json()["id"]
        
        # Add transactions to both portfolios
        transaction1 = {
            "portfolio_id": portfolio1_id,
            "asset_id": asset_id,
            "transaction_type": "buy",
            "quantity": "5.0",
            "price": "80.00",
            "total_amount": "400.00",
            "transaction_date": "2024-01-15T10:00:00"
        }
        
        transaction2 = {
            "portfolio_id": portfolio2_id,
            "asset_id": asset_id,
            "transaction_type": "buy",
            "quantity": "10.0",
            "price": "80.00",
            "total_amount": "800.00",
            "transaction_date": "2024-01-15T10:00:00"
        }
        
        client.post("/api/v1/transactions/", json=transaction1)
        client.post("/api/v1/transactions/", json=transaction2)
        
        # Check holdings are isolated
        holdings1_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio1_id}")
        holdings2_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio2_id}")
        
        holdings1 = holdings1_response.json()
        holdings2 = holdings2_response.json()
        
        assert len(holdings1) == 1
        assert len(holdings2) == 1
        assert holdings1[0]["quantity"] == "5.0"
        assert holdings2[0]["quantity"] == "10.0"
        
        # Check performance is isolated
        performance1_response = client.get(f"/api/v1/portfolios/{portfolio1_id}/performance")
        performance2_response = client.get(f"/api/v1/portfolios/{portfolio2_id}/performance")
        
        performance1 = performance1_response.json()
        performance2 = performance2_response.json()
        
        assert performance1["total_value"] == 400.0
        assert performance2["total_value"] == 800.0