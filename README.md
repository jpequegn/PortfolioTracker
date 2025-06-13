# Portfolio Tracker Backend

A comprehensive Python backend for portfolio tracking application that allows you to store and track performance of stocks, bonds, ETFs, and cash holdings.

## Features

- **Multi-Asset Support**: Track stocks, bonds, ETFs, cash, and other asset types
- **Portfolio Management**: Create and manage multiple portfolios
- **Transaction Tracking**: Record buy/sell transactions with automatic holding updates
- **Performance Analytics**: Calculate portfolio value, gains/losses, and returns
- **Diversification Analysis**: Analyze portfolio allocation by asset type and individual holdings
- **Real-time Price Updates**: Integration with Yahoo Finance for current market prices
- **RESTful API**: Complete REST API with automatic documentation

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Default database (easily configurable for PostgreSQL/MySQL)
- **yfinance**: Yahoo Finance API for real-time price data
- **Uvicorn**: ASGI server for running the application

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PortfolioTracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Quick Start

1. **Create sample data** (optional):
```bash
python create_sample_data.py
```

2. **Start the server**:
```bash
python main.py
```

The API will be available at:
- Main API: http://localhost:12000
- Interactive docs: http://localhost:12000/docs
- ReDoc: http://localhost:12000/redoc

3. **Test the API**:
```bash
python test_api.py
```

## API Endpoints

### Portfolios
- `GET /api/v1/portfolios/` - List all portfolios
- `POST /api/v1/portfolios/` - Create a new portfolio
- `GET /api/v1/portfolios/{id}` - Get portfolio with holdings
- `PUT /api/v1/portfolios/{id}` - Update portfolio
- `DELETE /api/v1/portfolios/{id}` - Delete portfolio
- `GET /api/v1/portfolios/{id}/performance` - Get performance metrics
- `GET /api/v1/portfolios/{id}/diversification` - Get diversification analysis

### Assets
- `GET /api/v1/assets/` - List all assets
- `POST /api/v1/assets/` - Create a new asset
- `GET /api/v1/assets/search?q={query}` - Search assets
- `GET /api/v1/assets/lookup/{symbol}` - Lookup asset info from external source
- `POST /api/v1/assets/lookup/{symbol}/create` - Create asset from lookup
- `GET /api/v1/assets/{id}` - Get specific asset
- `PUT /api/v1/assets/{id}` - Update asset
- `DELETE /api/v1/assets/{id}` - Delete asset
- `POST /api/v1/assets/update-prices` - Update current prices

### Holdings
- `GET /api/v1/holdings/` - List holdings (optionally by portfolio)
- `POST /api/v1/holdings/` - Create a new holding
- `GET /api/v1/holdings/{id}` - Get specific holding
- `PUT /api/v1/holdings/{id}` - Update holding
- `DELETE /api/v1/holdings/{id}` - Delete holding

### Transactions
- `GET /api/v1/transactions/` - List transactions (optionally by portfolio/asset)
- `POST /api/v1/transactions/` - Create transaction (automatically updates holdings)
- `GET /api/v1/transactions/{id}` - Get specific transaction
- `PUT /api/v1/transactions/{id}` - Update transaction
- `DELETE /api/v1/transactions/{id}` - Delete transaction

## Data Models

### Portfolio
- Multiple portfolios support
- Name and description
- Automatic timestamps

### Asset
- Symbol, name, and type (stock, bond, ETF, cash, etc.)
- Exchange and currency information
- Current price tracking
- Last updated timestamp

### Holding
- Links portfolio to asset
- Quantity and average cost tracking
- Automatic updates via transactions

### Transaction
- Complete transaction history
- Buy/sell/dividend/deposit/withdrawal types
- Price, quantity, fees, and total amount
- Automatic holding updates

## Performance Metrics

The system calculates various performance metrics:

- **Total Portfolio Value**: Current market value of all holdings
- **Total Cost Basis**: Total amount invested
- **Gain/Loss**: Absolute and percentage returns
- **Asset Allocation**: Breakdown by asset type and individual holdings
- **Diversification Analysis**: Portfolio distribution metrics

## Example Usage

### Creating a Portfolio
```python
import requests

portfolio_data = {
    "name": "My Investment Portfolio",
    "description": "Long-term growth portfolio"
}

response = requests.post(
    "http://localhost:12000/api/v1/portfolios/",
    json=portfolio_data
)
portfolio = response.json()
```

### Adding a Transaction
```python
transaction_data = {
    "portfolio_id": 1,
    "asset_id": 1,
    "transaction_type": "buy",
    "quantity": "10.0",
    "price": "150.00",
    "total_amount": "1500.00",
    "transaction_date": "2024-01-15T10:00:00",
    "notes": "Initial purchase"
}

response = requests.post(
    "http://localhost:12000/api/v1/transactions/",
    json=transaction_data
)
```

### Getting Portfolio Performance
```python
response = requests.get(
    "http://localhost:12000/api/v1/portfolios/1/performance"
)
performance = response.json()
print(f"Total Value: ${performance['total_value']}")
print(f"Total Gain/Loss: ${performance['total_gain_loss']}")
```

## Configuration

Environment variables in `.env`:

- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: Secret key for security
- `ALPHA_VANTAGE_API_KEY`: API key for Alpha Vantage (optional)
- `DEBUG`: Enable debug mode

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
The application uses SQLAlchemy with automatic table creation. For production, consider using Alembic for migrations:

```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Production Deployment

1. Set `DEBUG=False` in environment
2. Use a production database (PostgreSQL recommended)
3. Set up proper secret key
4. Use a production ASGI server like Gunicorn with Uvicorn workers
5. Set up reverse proxy (nginx)
6. Configure SSL/TLS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.