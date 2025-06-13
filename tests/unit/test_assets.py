"""
Unit tests for asset endpoints
"""
import pytest
from fastapi import status
from unittest.mock import patch, MagicMock


class TestAssetEndpoints:
    """Test asset CRUD operations"""

    def test_create_asset(self, client, sample_asset_data):
        """Test creating a new asset"""
        response = client.post("/api/v1/assets/", json=sample_asset_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["symbol"] == sample_asset_data["symbol"]
        assert data["name"] == sample_asset_data["name"]
        assert data["asset_type"] == sample_asset_data["asset_type"]
        assert "id" in data

    def test_get_assets(self, client, sample_asset_data):
        """Test getting all assets"""
        # Create an asset first
        client.post("/api/v1/assets/", json=sample_asset_data)
        
        response = client.get("/api/v1/assets/")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_asset_by_id(self, client, sample_asset_data):
        """Test getting a specific asset"""
        # Create an asset first
        create_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/assets/{asset_id}")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["id"] == asset_id
        assert data["symbol"] == sample_asset_data["symbol"]

    def test_search_assets(self, client, sample_asset_data):
        """Test searching assets"""
        # Create an asset first
        client.post("/api/v1/assets/", json=sample_asset_data)
        
        response = client.get("/api/v1/assets/search?q=AAPL")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)

    def test_update_asset(self, client, sample_asset_data):
        """Test updating an asset"""
        # Create an asset first
        create_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = create_response.json()["id"]
        
        # Update the asset
        updated_data = {
            **sample_asset_data,
            "current_price": "160.00"
        }
        response = client.put(f"/api/v1/assets/{asset_id}", json=updated_data)
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["current_price"] == "160.00"

    def test_delete_asset(self, client, sample_asset_data):
        """Test deleting an asset"""
        # Create an asset first
        create_response = client.post("/api/v1/assets/", json=sample_asset_data)
        asset_id = create_response.json()["id"]
        
        # Delete the asset
        response = client.delete(f"/api/v1/assets/{asset_id}")
        assert response.status_code == status.HTTP_200_OK
        
        # Verify it's deleted
        get_response = client.get(f"/api/v1/assets/{asset_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    @patch('app.services.price_service.get_asset_info')
    def test_lookup_asset(self, mock_get_asset_info, client):
        """Test looking up asset information"""
        # Mock the external API response
        mock_get_asset_info.return_value = {
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "asset_type": "stock",
            "exchange": "NASDAQ",
            "currency": "USD",
            "current_price": 150.00
        }
        
        response = client.get("/api/v1/assets/lookup/AAPL")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["symbol"] == "AAPL"
        assert data["name"] == "Apple Inc."

    @patch('app.services.price_service.get_asset_info')
    def test_create_asset_from_lookup(self, mock_get_asset_info, client):
        """Test creating an asset from lookup data"""
        # Mock the external API response
        mock_get_asset_info.return_value = {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "asset_type": "stock",
            "exchange": "NASDAQ",
            "currency": "USD",
            "current_price": 300.00
        }
        
        response = client.post("/api/v1/assets/lookup/MSFT/create")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert data["symbol"] == "MSFT"
        assert data["name"] == "Microsoft Corporation"

    def test_create_asset_invalid_data(self, client):
        """Test creating asset with invalid data"""
        invalid_data = {"name": "Missing symbol field"}
        response = client.post("/api/v1/assets/", json=invalid_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_get_nonexistent_asset(self, client):
        """Test getting an asset that doesn't exist"""
        response = client.get("/api/v1/assets/99999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('app.services.price_service.update_asset_prices')
    def test_update_asset_prices(self, mock_update_prices, client):
        """Test updating asset prices"""
        mock_update_prices.return_value = {"updated_count": 5}
        
        response = client.post("/api/v1/assets/update-prices")
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert "updated_count" in data