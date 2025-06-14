import yfinance as yf
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.crud.asset import asset
from app.models.asset import AssetType
import pandas as pd


class PriceService:
    @staticmethod
    def get_current_price(symbol: str) -> Optional[Decimal]:
        """Get current price for a single symbol using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            if price:
                return Decimal(str(price))
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
        return None

    @staticmethod
    def get_multiple_prices(symbols: List[str]) -> Dict[str, Optional[Decimal]]:
        """Get current prices for multiple symbols"""
        prices = {}
        for symbol in symbols:
            prices[symbol] = PriceService.get_current_price(symbol)
        return prices

    @staticmethod
    def update_asset_prices(db: Session, asset_ids: Optional[List[int]] = None):
        """Update prices for assets in the database"""
        if asset_ids:
            assets = [asset.get(db, id=asset_id) for asset_id in asset_ids]
            assets = [a for a in assets if a is not None]
        else:
            assets = asset.get_multi(db, limit=1000)

        # Filter out cash assets as they don't have market prices
        tradeable_assets = [a for a in assets if a.asset_type != AssetType.CASH]
        
        symbols = [a.symbol for a in tradeable_assets]
        prices = PriceService.get_multiple_prices(symbols)

        for asset_obj in tradeable_assets:
            new_price = prices.get(asset_obj.symbol)
            if new_price:
                asset.update(
                    db,
                    db_obj=asset_obj,
                    obj_in={
                        "current_price": new_price,
                        "last_updated": datetime.utcnow()
                    }
                )

    @staticmethod
    def get_asset_info(symbol: str) -> Dict:
        """Get detailed asset information from yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Determine asset type based on available info
            asset_type = AssetType.STOCK  # default
            if 'fundFamily' in info or 'category' in info:
                asset_type = AssetType.ETF
            elif 'bondRating' in info or 'maturityDate' in info:
                asset_type = AssetType.BOND
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', info.get('shortName', symbol)),
                'asset_type': asset_type,
                'exchange': info.get('exchange'),
                'currency': info.get('currency', 'USD'),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice')),
                'sector': info.get('sector'),
                'industry': info.get('industry')
            }
        except Exception as e:
            print(f"Error fetching asset info for {symbol}: {e}")
            return {
                'symbol': symbol.upper(),
                'name': symbol.upper(),
                'asset_type': AssetType.STOCK,
                'currency': 'USD'
            }

    @staticmethod
    def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d") -> Dict:
        """
        Get historical market data for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            Dictionary containing historical data and metadata
        """
        try:
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period=period, interval=interval)
            
            if hist.empty:
                return {
                    'symbol': symbol.upper(),
                    'error': 'No data available for this symbol',
                    'data': []
                }
            
            # Convert to list of dictionaries for JSON serialization
            data = []
            for date, row in hist.iterrows():
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']),
                    'high': float(row['High']),
                    'low': float(row['Low']),
                    'close': float(row['Close']),
                    'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0
                })
            
            # Get basic info about the stock
            info = ticker.info
            
            # Calculate some basic statistics
            closes = [d['close'] for d in data]
            if len(closes) > 1:
                current_price = closes[-1]
                previous_price = closes[-2]
                change = current_price - previous_price
                change_percent = (change / previous_price) * 100 if previous_price != 0 else 0
                
                period_start_price = closes[0]
                period_change = current_price - period_start_price
                period_change_percent = (period_change / period_start_price) * 100 if period_start_price != 0 else 0
            else:
                change = 0
                change_percent = 0
                period_change = 0
                period_change_percent = 0
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', info.get('shortName', symbol.upper())),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', ''),
                'period': period,
                'interval': interval,
                'current_price': closes[-1] if closes else None,
                'daily_change': change,
                'daily_change_percent': change_percent,
                'period_change': period_change,
                'period_change_percent': period_change_percent,
                'data': data,
                'data_points': len(data)
            }
            
        except Exception as e:
            return {
                'symbol': symbol.upper(),
                'error': f'Error fetching historical data: {str(e)}',
                'data': []
            }