"""
Unit tests for portfolio endpoints
"""
import pytest
from fastapi import status


class TestPortfolioEndpoints:
    """Test portfolio CRUD operations"""

    def test_create_portfolio(self, client, sample_portfolio_data):
        """Test creating a new portfolio"""
        response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["name"] == sample_portfolio_data["name"]
        assert data["description"] == sample_portfolio_data["description"]
        assert "id" in data
        assert "created_at" in data

    def test_get_portfolios(self, client, sample_portfolio_data):
        """Test getting all portfolios"""
        # Create a portfolio first
        client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        
        response = client.get("/api/v1/portfolios/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_portfolio_by_id(self, client, sample_portfolio_data):
        """Test getting a specific portfolio"""
        # Create a portfolio first
        create_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/portfolios/{portfolio_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == portfolio_id
        assert data["name"] == sample_portfolio_data["name"]

    def test_get_nonexistent_portfolio(self, client):
        """Test getting a portfolio that doesn't exist"""
        response = client.get("/api/v1/portfolios/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_portfolio(self, client, sample_portfolio_data):
        """Test updating a portfolio"""
        # Create a portfolio first
        create_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = create_response.json()["id"]
        
        # Update the portfolio
        updated_data = {
            "name": "Updated Portfolio",
            "description": "Updated description"
        }
        response = client.put(f"/api/v1/portfolios/{portfolio_id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["name"] == updated_data["name"]
        assert data["description"] == updated_data["description"]

    def test_delete_portfolio(self, client, sample_portfolio_data):
        """Test deleting a portfolio"""
        # Create a portfolio first
        create_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = create_response.json()["id"]
        
        # Delete the portfolio
        response = client.delete(f"/api/v1/portfolios/{portfolio_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/portfolios/{portfolio_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_portfolio_performance_empty(self, client, sample_portfolio_data):
        """Test getting performance for an empty portfolio"""
        # Create a portfolio first
        create_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/portfolios/{portfolio_id}/performance")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["total_value"] == 0.0
        assert data["total_cost_basis"] == 0.0
        assert data["total_gain_loss"] == 0.0

    def test_get_portfolio_diversification_empty(self, client, sample_portfolio_data):
        """Test getting diversification for an empty portfolio"""
        # Create a portfolio first
        create_response = client.post("/api/v1/portfolios/", json=sample_portfolio_data)
        portfolio_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/portfolios/{portfolio_id}/diversification")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "by_asset_type" in data
        assert "by_holding" in data

    def test_create_portfolio_invalid_data(self, client):
        """Test creating portfolio with invalid data"""
        invalid_data = {"description": "Missing name field"}
        response = client.post("/api/v1/portfolios/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY