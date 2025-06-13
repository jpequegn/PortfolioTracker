# Portfolio Tracker API Documentation

## Overview

The Portfolio Tracker API is a comprehensive backend system built with FastAPI that allows users to track their investment portfolios including stocks, bonds, ETFs, and cash holdings. The system provides real-time performance tracking, diversification analysis, and transaction management.

## Features

- **Multi-Asset Support**: Track stocks, bonds, ETFs, and cash holdings
- **Real-time Price Updates**: Automatic price fetching from Yahoo Finance
- **Performance Analytics**: Calculate gains/losses, returns, and performance metrics
- **Diversification Analysis**: Asset allocation and portfolio composition analysis
- **Transaction Management**: Buy/sell transactions with automatic holding updates
- **Portfolio Management**: Multiple portfolio support with detailed tracking

## API Endpoints

### Health Check
- `GET /health` - API health status

### Portfolios
- `GET /api/v1/portfolios/` - List all portfolios
- `POST /api/v1/portfolios/` - Create a new portfolio
- `GET /api/v1/portfolios/{id}` - Get portfolio with holdings
- `PUT /api/v1/portfolios/{id}` - Update portfolio
- `DELETE /api/v1/portfolios/{id}` - Delete portfolio
- `GET /api/v1/portfolios/{id}/performance` - Get portfolio performance metrics
- `GET /api/v1/portfolios/{id}/diversification` - Get portfolio diversification analysis

### Assets
- `GET /api/v1/assets/` - List all assets
- `POST /api/v1/assets/` - Create a new asset
- `GET /api/v1/assets/{id}` - Get specific asset
- `PUT /api/v1/assets/{id}` - Update asset
- `DELETE /api/v1/assets/{id}` - Delete asset
- `GET /api/v1/assets/lookup/{symbol}` - Lookup asset by symbol
- `POST /api/v1/assets/update-prices` - Update asset prices

### Holdings
- `GET /api/v1/holdings/` - List holdings (with optional portfolio filter)
- `POST /api/v1/holdings/` - Create a new holding
- `GET /api/v1/holdings/{id}` - Get specific holding
- `PUT /api/v1/holdings/{id}` - Update holding
- `DELETE /api/v1/holdings/{id}` - Delete holding

### Transactions
- `GET /api/v1/transactions/` - List transactions (with optional portfolio filter)
- `POST /api/v1/transactions/` - Create a new transaction (automatically updates holdings)
- `GET /api/v1/transactions/{id}` - Get specific transaction
- `PUT /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction

## Data Models

### Portfolio
```json
{
  "id": 1,
  "name": "Growth Portfolio",
  "description": "Long-term growth focused portfolio",
  "created_at": "2025-06-13T10:11:14",
  "updated_at": null
}
```

### Asset
```json
{
  "id": 1,
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "asset_type": "stock",
  "exchange": "NASDAQ",
  "currency": "USD",
  "current_price": "199.2000",
  "last_updated": "2025-06-13T10:18:10.346716",
  "created_at": "2025-06-13T10:11:14"
}
```

### Holding
```json
{
  "id": 1,
  "portfolio_id": 1,
  "asset_id": 1,
  "quantity": "20.000000",
  "average_cost": "150.0000",
  "created_at": "2025-06-13T10:17:42",
  "updated_at": "2025-06-13T10:18:03",
  "asset": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "asset_type": "stock",
    "exchange": "NASDAQ",
    "currency": "USD",
    "current_price": "199.2000"
  }
}
```

### Transaction
```json
{
  "id": 2,
  "portfolio_id": 1,
  "asset_id": 1,
  "transaction_type": "buy",
  "quantity": "10.000000",
  "price": "150.0000",
  "fees": "0.0000",
  "total_amount": "1500.0000",
  "transaction_date": "2025-06-13T10:00:00",
  "notes": null,
  "created_at": "2025-06-13T10:18:03"
}
```

### Performance Metrics
```json
{
  "portfolio_id": 1,
  "total_value": 12769.0,
  "total_cost": 4000.0,
  "total_gain_loss": 8769.0,
  "total_gain_loss_percent": 219.225,
  "holdings": [
    {
      "asset": {
        "id": 1,
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "asset_type": "stock"
      },
      "quantity": 20.0,
      "average_cost": 150.0,
      "current_price": 199.2,
      "current_value": 3984.0,
      "cost_basis": 3000.0,
      "gain_loss": 984.0,
      "gain_loss_percent": 32.8
    }
  ]
}
```

### Diversification Analysis
```json
{
  "total_value": 12769.0,
  "by_asset_type": {
    "stock": 100
  },
  "by_asset": [
    {
      "asset": {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "asset_type": "stock"
      },
      "value": 3984.0,
      "percentage": 31.20056386561203
    }
  ]
}
```

## Asset Types

The system supports the following asset types:
- `stock` - Individual stocks
- `bond` - Government and corporate bonds
- `etf` - Exchange-traded funds
- `cash` - Cash holdings

## Transaction Types

- `buy` - Purchase assets
- `sell` - Sell assets
- `dividend` - Dividend payments
- `split` - Stock splits
- `deposit` - Cash deposits
- `withdrawal` - Cash withdrawals

## Example Usage

### Creating a Portfolio
```bash
curl -X POST http://localhost:12000/api/v1/portfolios/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Portfolio",
    "description": "Personal investment portfolio"
  }'
```

### Adding a Transaction
```bash
curl -X POST http://localhost:12000/api/v1/transactions/ \
  -H "Content-Type: application/json" \
  -d '{
    "portfolio_id": 1,
    "asset_id": 1,
    "transaction_type": "buy",
    "quantity": 10,
    "price": 150.00,
    "total_amount": 1500.00,
    "transaction_date": "2025-06-13T10:00:00Z"
  }'
```

### Getting Portfolio Performance
```bash
curl http://localhost:12000/api/v1/portfolios/1/performance
```

## Technical Details

- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: SQLite (easily configurable for PostgreSQL/MySQL)
- **Price Data**: Yahoo Finance API via yfinance
- **Validation**: Pydantic models for request/response validation
- **CORS**: Enabled for frontend integration

## Running the Application

1. Install dependencies: `pip install -r requirements.txt`
2. Initialize database: `python init_db.py`
3. Create sample data: `python create_sample_data.py`
4. Start server: `python main.py`
5. Access API docs: `http://localhost:12000/docs`

The API is now ready for frontend integration and provides a complete backend solution for portfolio tracking applications.