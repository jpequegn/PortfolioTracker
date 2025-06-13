import yfinance as yf
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud.asset import asset
from app.models.asset import AssetType


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