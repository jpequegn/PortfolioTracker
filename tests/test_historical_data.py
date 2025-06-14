import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


class TestHistoricalDataEndpoint:
    """Test the historical data endpoint"""

    @patch('app.services.price_service.PriceService.get_historical_data')
    def test_get_historical_data_success(self, mock_get_historical_data):
        """Test successful historical data retrieval"""
        # Mock the response from PriceService
        mock_data = {
            'symbol': 'AAPL',
            'name': 'Apple Inc.',
            'currency': 'USD',
            'exchange': 'NASDAQ',
            'period': '1y',
            'interval': '1d',
            'current_price': 150.0,
            'daily_change': 2.5,
            'daily_change_percent': 1.69,
            'period_change': 25.0,
            'period_change_percent': 20.0,
            'data': [
                {
                    'date': '2023-01-01',
                    'open': 148.0,
                    'high': 152.0,
                    'low': 147.0,
                    'close': 150.0,
                    'volume': 1000000
                }
            ],
            'data_points': 1
        }
        mock_get_historical_data.return_value = mock_data

        # Make the API call
        response = client.get("/api/v1/assets/AAPL/historical")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['symbol'] == 'AAPL'
        assert data['name'] == 'Apple Inc.'
        assert data['current_price'] == 150.0
        assert len(data['data']) == 1
        assert data['data'][0]['close'] == 150.0

    @patch('app.services.price_service.PriceService.get_historical_data')
    def test_get_historical_data_with_parameters(self, mock_get_historical_data):
        """Test historical data retrieval with custom parameters"""
        mock_data = {
            'symbol': 'MSFT',
            'name': 'Microsoft Corporation',
            'currency': 'USD',
            'exchange': 'NASDAQ',
            'period': '6mo',
            'interval': '1wk',
            'current_price': 300.0,
            'daily_change': 5.0,
            'daily_change_percent': 1.69,
            'period_change': 50.0,
            'period_change_percent': 20.0,
            'data': [],
            'data_points': 0
        }
        mock_get_historical_data.return_value = mock_data

        # Make the API call with parameters
        response = client.get("/api/v1/assets/MSFT/historical?period=6mo&interval=1wk")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data['symbol'] == 'MSFT'
        assert data['period'] == '6mo'
        assert data['interval'] == '1wk'

    @patch('app.services.price_service.PriceService.get_historical_data')
    def test_get_historical_data_error(self, mock_get_historical_data):
        """Test historical data retrieval with error"""
        # Mock an error response
        mock_get_historical_data.return_value = {
            'symbol': 'INVALID',
            'error': 'No data available for this symbol',
            'data': []
        }

        # Make the API call
        response = client.get("/api/v1/assets/INVALID/historical")
        
        # Assertions
        assert response.status_code == 404
        assert "No data available for this symbol" in response.json()['detail']

    def test_get_historical_data_invalid_symbol(self):
        """Test historical data retrieval with invalid symbol"""
        # Make the API call with a clearly invalid symbol
        response = client.get("/api/v1/assets/INVALIDXYZ123/historical")
        
        # Should return 404 for invalid symbols
        assert response.status_code == 404


class TestPriceServiceHistoricalData:
    """Test the PriceService historical data functionality"""

    @patch('yfinance.Ticker')
    def test_get_historical_data_success(self, mock_ticker):
        """Test successful historical data retrieval from PriceService"""
        from app.services.price_service import PriceService
        import pandas as pd
        from datetime import datetime

        # Mock yfinance Ticker
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance

        # Mock historical data
        mock_hist = pd.DataFrame({
            'Open': [148.0, 149.0],
            'High': [152.0, 153.0],
            'Low': [147.0, 148.0],
            'Close': [150.0, 151.0],
            'Volume': [1000000, 1100000]
        }, index=[datetime(2023, 1, 1), datetime(2023, 1, 2)])
        
        mock_ticker_instance.history.return_value = mock_hist
        mock_ticker_instance.info = {
            'longName': 'Apple Inc.',
            'currency': 'USD',
            'exchange': 'NASDAQ'
        }

        # Call the method
        result = PriceService.get_historical_data('AAPL', '1y', '1d')

        # Assertions
        assert result['symbol'] == 'AAPL'
        assert result['name'] == 'Apple Inc.'
        assert result['currency'] == 'USD'
        assert result['exchange'] == 'NASDAQ'
        assert result['period'] == '1y'
        assert result['interval'] == '1d'
        assert len(result['data']) == 2
        assert result['data'][0]['close'] == 150.0
        assert result['data'][1]['close'] == 151.0
        assert result['current_price'] == 151.0
        assert result['daily_change'] == 1.0
        assert 'error' not in result

    @patch('yfinance.Ticker')
    def test_get_historical_data_empty_response(self, mock_ticker):
        """Test historical data retrieval with empty response"""
        from app.services.price_service import PriceService
        import pandas as pd

        # Mock yfinance Ticker
        mock_ticker_instance = MagicMock()
        mock_ticker.return_value = mock_ticker_instance

        # Mock empty historical data
        mock_ticker_instance.history.return_value = pd.DataFrame()

        # Call the method
        result = PriceService.get_historical_data('INVALID', '1y', '1d')

        # Assertions
        assert result['symbol'] == 'INVALID'
        assert result['error'] == 'No data available for this symbol'
        assert result['data'] == []

    @patch('yfinance.Ticker')
    def test_get_historical_data_exception(self, mock_ticker):
        """Test historical data retrieval with exception"""
        from app.services.price_service import PriceService

        # Mock yfinance Ticker to raise an exception
        mock_ticker.side_effect = Exception("Network error")

        # Call the method
        result = PriceService.get_historical_data('AAPL', '1y', '1d')

        # Assertions
        assert result['symbol'] == 'AAPL'
        assert 'error' in result
        assert 'Network error' in result['error']
        assert result['data'] == []