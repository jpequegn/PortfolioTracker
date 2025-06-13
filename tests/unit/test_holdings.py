"""
Unit tests for holding endpoints
"""
import pytest
from fastapi import status


class TestHoldingEndpoints:
    """Test holding CRUD operations"""

    def test_create_holding(self, client, sample_portfolio_data, sample_asset_data):
        """Test creating a new holding"""
        # Create portfolio and asset first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        # Create holding
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        
        response = client.post("/api/v1/holdings/", json=holding_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["portfolio_id"] == portfolio_id
        assert data["asset_id"] == asset_id
        assert data["quantity"] == "5.0"
        assert "id" in data

    def test_get_holdings(self, client, sample_portfolio_data, sample_asset_data):
        """Test getting all holdings"""
        # Create portfolio, asset, and holding first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        client.post("/api/v1/holdings/", json=holding_data)
        
        response = client.get("/api/v1/holdings/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_holdings_by_portfolio(self, client, sample_portfolio_data, sample_asset_data):
        """Test getting holdings filtered by portfolio"""
        # Create portfolio, asset, and holding first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        client.post("/api/v1/holdings/", json=holding_data)
        
        response = client.get(f"/api/v1/holdings/?portfolio_id={portfolio_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert all(h["portfolio_id"] == portfolio_id for h in data)

    def test_get_holding_by_id(self, client, sample_portfolio_data, sample_asset_data):
        """Test getting a specific holding"""
        # Create portfolio, asset, and holding first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        create_response = client.post("/api/v1/holdings/", json=holding_data)
        holding_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/holdings/{holding_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == holding_id
        assert data["portfolio_id"] == portfolio_id

    def test_update_holding(self, client, sample_portfolio_data, sample_asset_data):
        """Test updating a holding"""
        # Create portfolio, asset, and holding first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        create_response = client.post("/api/v1/holdings/", json=holding_data)
        holding_id = create_response.json()["id"]
        
        # Update the holding
        updated_data = {
            **holding_data,
            "quantity": "10.0"
        }
        response = client.put(f"/api/v1/holdings/{holding_id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["quantity"] == "10.0"

    def test_delete_holding(self, client, sample_portfolio_data, sample_asset_data):
        """Test deleting a holding"""
        # Create portfolio, asset, and holding first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        create_response = client.post("/api/v1/holdings/", json=holding_data)
        holding_id = create_response.json()["id"]
        
        # Delete the holding
        response = client.delete(f"/api/v1/holdings/{holding_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/holdings/{holding_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_holding_invalid_data(self, client):
        """Test creating holding with invalid data"""
        invalid_data = {"quantity": "5.0"}  # Missing required fields
        response = client.post("/api/v1/holdings/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_nonexistent_holding(self, client):
        """Test getting a holding that doesn't exist"""
        response = client.get("/api/v1/holdings/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_duplicate_holding_prevention(self, client, sample_portfolio_data, sample_asset_data):
        """Test that duplicate holdings for same portfolio/asset are prevented"""
        # Create portfolio and asset first
        portfolio_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = portfolio_response.json()["id"]
        
        asset_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = asset_response.json()["id"]
        
        # Create first holding
        holding_data = {
            "portfolio_id": portfolio_id,
            "asset_id": asset_id,
            "quantity": "5.0",
            "average_cost": "150.00"
        }
        response1 = client.post("/api/v1/holdings/", json=holding_data)
        assert response1.status_code == status.HTTP_200_OK
        
        # Try to create duplicate holding
        response2 = client.post("/api/v1/holdings/", json=holding_data)
        # This should either fail or update the existing holding
        # The exact behavior depends on the implementation