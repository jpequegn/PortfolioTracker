"""
Unit tests for service layer
"""
import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal

from app.services.portfolio_service import PortfolioService
from app.services.price_service import get_asset_info, update_asset_prices


class TestPortfolioService:
    """Test portfolio service calculations"""

    def test_calculate_portfolio_performance_empty(self):
        """Test performance calculation for empty portfolio"""
        holdings = []
        performance = PortfolioService.calculate_performance(holdings)
        
        assert performance["total_value"] == 0.0
        assert performance["total_cost_basis"] == 0.0
        assert performance["total_gain_loss"] == 0.0
        assert performance["total_gain_loss_percentage"] == 0.0

    def test_calculate_portfolio_performance_with_holdings(self):
        """Test performance calculation with holdings"""
        # Mock holdings data
        holdings = [
            {
                "quantity": Decimal("10.0"),
                "average_cost": Decimal("100.0"),
                "asset": {"current_price": Decimal("120.0")}
            },
            {
                "quantity": Decimal("5.0"),
                "average_cost": Decimal("200.0"),
                "asset": {"current_price": Decimal("180.0")}
            }
        ]
        
        performance = PortfolioService.calculate_performance(holdings)
        
        # Total value: (10 * 120) + (5 * 180) = 2100
        # Total cost: (10 * 100) + (5 * 200) = 2000
        # Gain/Loss: 2100 - 2000 = 100
        # Percentage: (100 / 2000) * 100 = 5%
        
        assert performance["total_value"] == 2100.0
        assert performance["total_cost_basis"] == 2000.0
        assert performance["total_gain_loss"] == 100.0
        assert performance["total_gain_loss_percentage"] == 5.0

    def test_calculate_diversification_by_asset_type(self):
        """Test diversification calculation by asset type"""
        holdings = [
            {
                "quantity": Decimal("10.0"),
                "asset": {
                    "current_price": Decimal("100.0"),
                    "asset_type": "stock"
                }
            },
            {
                "quantity": Decimal("5.0"),
                "asset": {
                    "current_price": Decimal("200.0"),
                    "asset_type": "stock"
                }
            },
            {
                "quantity": Decimal("500.0"),
                "asset": {
                    "current_price": Decimal("1.0"),
                    "asset_type": "cash"
                }
            }
        ]
        
        diversification = PortfolioService.calculate_diversification(holdings)
        
        # Total value: (10 * 100) + (5 * 200) + (500 * 1) = 2500
        # Stock value: 1000 + 1000 = 2000 (80%)
        # Cash value: 500 (20%)
        
        by_asset_type = diversification["by_asset_type"]
        stock_allocation = next(item for item in by_asset_type if item["asset_type"] == "stock")
        cash_allocation = next(item for item in by_asset_type if item["asset_type"] == "cash")
        
        assert stock_allocation["percentage"] == 80.0
        assert cash_allocation["percentage"] == 20.0

    def test_calculate_diversification_by_holding(self):
        """Test diversification calculation by individual holding"""
        holdings = [
            {
                "quantity": Decimal("10.0"),
                "asset": {
                    "current_price": Decimal("100.0"),
                    "symbol": "AAPL",
                    "name": "Apple Inc."
                }
            },
            {
                "quantity": Decimal("5.0"),
                "asset": {
                    "current_price": Decimal("200.0"),
                    "symbol": "GOOGL",
                    "name": "Alphabet Inc."
                }
            }
        ]
        
        diversification = PortfolioService.calculate_diversification(holdings)
        
        # Total value: (10 * 100) + (5 * 200) = 2000
        # AAPL: 1000 (50%)
        # GOOGL: 1000 (50%)
        
        by_holding = diversification["by_holding"]
        assert len(by_holding) == 2
        
        for holding in by_holding:
            assert holding["percentage"] == 50.0


class TestPriceService:
    """Test price service functionality"""

    @patch('yfinance.Ticker')
    def test_get_asset_info_success(self, mock_ticker):
        """Test successful asset info retrieval"""
        # Mock yfinance response
        mock_info = {
            'symbol': 'AAPL',
            'longName': 'Apple Inc.',
            'quoteType': 'EQUITY',
            'exchange': 'NMS',
            'currency': 'USD',
            'regularMarketPrice': 150.0
        }
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = mock_info
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_asset_info('AAPL')
        
        assert result['symbol'] == 'AAPL'
        assert result['name'] == 'Apple Inc.'
        assert result['asset_type'] == 'stock'
        assert result['exchange'] == 'NMS'
        assert result['currency'] == 'USD'
        assert result['current_price'] == 150.0

    @patch('yfinance.Ticker')
    def test_get_asset_info_not_found(self, mock_ticker):
        """Test asset info retrieval for non-existent symbol"""
        # Mock yfinance response for invalid symbol
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = {}
        mock_ticker.return_value = mock_ticker_instance
        
        result = get_asset_info('INVALID')
        
        assert result is None

    @patch('yfinance.Ticker')
    def test_get_asset_info_exception(self, mock_ticker):
        """Test asset info retrieval with exception"""
        # Mock yfinance to raise an exception
        mock_ticker.side_effect = Exception("Network error")
        
        result = get_asset_info('AAPL')
        
        assert result is None

    def test_map_quote_type_to_asset_type(self):
        """Test mapping of yfinance quote types to our asset types"""
        from app.services.price_service import _map_quote_type_to_asset_type
        
        assert _map_quote_type_to_asset_type('EQUITY') == 'stock'
        assert _map_quote_type_to_asset_type('ETF') == 'etf'
        assert _map_quote_type_to_asset_type('MUTUALFUND') == 'mutual_fund'
        assert _map_quote_type_to_asset_type('BOND') == 'bond'
        assert _map_quote_type_to_asset_type('UNKNOWN') == 'other'