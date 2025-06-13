"""
Unit tests for transaction endpoints
"""
import pytest
from fastapi import status
from decimal import Decimal


class TestTransactionEndpoints:
    """Test transaction CRUD operations"""

    def test_create_transaction(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test creating a new transaction"""
        # Create portfolio and asset first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        # Create transaction
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        
        response = client.post("/api/v1/transactions/", json=transaction_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["portfolio_id"] == portfolio_id
        assert data["asset_id"] == asset_id
        assert data["transaction_type"] == sample_transaction_data["transaction_type"]
        assert "id" in data

    def test_get_transactions(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test getting all transactions"""
        # Create portfolio, asset, and transaction first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        client.post("/api/v1/transactions/", json=transaction_data)
        
        response = client.get("/api/v1/transactions/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_transactions_by_portfolio(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test getting transactions filtered by portfolio"""
        # Create portfolio, asset, and transaction first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        client.post("/api/v1/transactions/", json=transaction_data)
        
        response = client.get(f"/api/v1/transactions/?portfolio_id={portfolio_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert all(t["portfolio_id"] == portfolio_id for t in data)

    def test_get_transaction_by_id(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test getting a specific transaction"""
        # Create portfolio, asset, and transaction first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        create_response = client.post("/api/v1/transactions/", json=transaction_data)
        transaction_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/transactions/{transaction_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == transaction_id
        assert data["portfolio_id"] == portfolio_id

    def test_update_transaction(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test updating a transaction"""
        # Create portfolio, asset, and transaction first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        create_response = client.post("/api/v1/transactions/", json=transaction_data)
        transaction_id = create_response.json()["id"]
        
        # Update the transaction
        updated_data = {
            **transaction_data,
            "notes": "Updated transaction notes"
        }
        response = client.put(f"/api/v1/transactions/{transaction_id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["notes"] == "Updated transaction notes"

    def test_delete_transaction(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test deleting a transaction"""
        # Create portfolio, asset, and transaction first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        create_response = client.post("/api/v1/transactions/", json=transaction_data)
        transaction_id = create_response.json()["id"]
        
        # Delete the transaction
        response = client.delete(f"/api/v1/transactions/{transaction_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/transactions/{transaction_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_transaction_creates_holding(self, client, sample_portfolio_data, sample_asset_data, sample_transaction_data):
        """Test that creating a transaction automatically creates/updates holdings"""
        # Create portfolio and asset first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        # Create transaction
        transaction_data = {
            **sample_transaction_data,
            "portfolio_id": portfolio_id,
            "asset_id": asset_id
        }
        
        response = client.post("/api/v1/transactions/", json=transaction_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Check that holding was created
        holdings_response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio_id}")
        assert holdings_response.status_code == status.HTTP_200_OK
        
        holdings = holdings_response.json()
        assert len(holdings) == 1
        assert holdings[0]["asset_id"] == asset_id
        assert holdings[0]["quantity"] == "10.0"

    def test_create_transaction_invalid_data(self, client):
        """Test creating transaction with invalid data"""
        invalid_data = {"transaction_type": "buy"}  # Missing required fields
        response = client.post("/api/v1/transactions/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_nonexistent_transaction(self, client):
        """Test getting a transaction that doesn't exist"""
        response = client.get("/api/v1/transactions/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND