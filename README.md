# Portfolio Tracker

A comprehensive full-stack portfolio tracking application that allows you to store and track performance of stocks, bonds, ETFs, and cash holdings. Built with a modern Python FastAPI backend and React TypeScript frontend.

## Features

- **Multi-Asset Support**: Track stocks, bonds, ETFs, cash, and other asset types
- **Portfolio Management**: Create and manage multiple portfolios
- **Transaction Tracking**: Record buy/sell transactions with automatic holding updates
- **Performance Analytics**: Calculate portfolio value, gains/losses, and returns
- **Diversification Analysis**: Analyze portfolio allocation by asset type and individual holdings
- **Real-time Price Updates**: Integration with Yahoo Finance for current market prices
- **RESTful API**: Complete REST API with automatic documentation

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Default database (easily configurable for PostgreSQL/MySQL)
- **yfinance**: Yahoo Finance API for real-time price data
- **Uvicorn**: ASGI server for running the application

### Frontend
- **React 19**: Modern React with latest features
- **TypeScript**: Type-safe JavaScript development
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Recharts**: Beautiful charts and data visualization
- **Axios**: HTTP client for API communication
- **Lucide React**: Beautiful icon library

### Testing
- **pytest**: Python testing framework
- **pytest-cov**: Coverage reporting
- **FastAPI TestClient**: API testing utilities
- **React Testing Library**: Frontend component testing
- **Jest**: JavaScript testing framework

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd PortfolioTracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Return to the project root:
```bash
cd ..
```

## Quick Start

### Option 1: Full Stack Development

1. **Start the backend server** (in one terminal):
```bash
python main.py
```

2. **Start the frontend development server** (in another terminal):
```bash
cd frontend
npm start
```

3. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:12000
- API Documentation: http://localhost:12000/docs

### Option 2: Backend Only

1. **Create sample data** (optional):
```bash
python create_sample_data.py
```

2. **Start the backend server**:
```bash
python main.py
```

3. **Access the API**:
- Main API: http://localhost:12000
- Interactive docs: http://localhost:12000/docs
- ReDoc: http://localhost:12000/redoc

4. **Test the API**:
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

## Testing

The project includes comprehensive test suites for both backend and frontend.

### Backend Tests

Run all backend tests:
```bash
python run_tests.py
```

Or run specific test types:
```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_portfolios.py -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Test Structure

```
tests/
├── conftest.py              # Test configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_portfolios.py   # Portfolio endpoint tests
│   ├── test_assets.py       # Asset endpoint tests
│   ├── test_transactions.py # Transaction endpoint tests
│   ├── test_holdings.py     # Holdings endpoint tests
│   └── test_services.py     # Service layer tests
└── integration/             # Integration tests
    └── test_portfolio_workflow.py  # End-to-end workflow tests

frontend/src/components/__tests__/  # Frontend component tests
```

### Test Coverage

The test suite covers:
- ✅ All API endpoints (CRUD operations)
- ✅ Business logic and calculations
- ✅ Error handling and edge cases
- ✅ Database operations
- ✅ Service layer functionality
- ✅ Integration workflows
- ✅ Frontend component rendering

### Testing Demo

To see the testing capabilities in action:
```bash
python demo_tests.py
```

This will demonstrate:
- Test infrastructure setup
- Basic test execution
- Test structure overview
- Coverage capabilities

## Development

### Backend Development

1. **Activate virtual environment**:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install development dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the development server**:
```bash
python main.py
```

### Frontend Development

1. **Start development server**:
```bash
cd frontend
npm start
```

2. **Build for production**:
```bash
npm run build
```

3. **Run frontend tests**:
```bash
npm test
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

## Project Structure

```
PortfolioTracker/
├── app/                     # Backend application
│   ├── api/                 # API routes and endpoints
│   ├── core/                # Core configuration and database
│   ├── crud/                # Database operations
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   └── services/            # Business logic services
├── frontend/                # React frontend application
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   └── App.tsx          # Main app component
│   └── package.json         # Frontend dependencies
├── tests/                   # Backend test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── conftest.py          # Test configuration
├── main.py                  # Backend entry point
├── requirements.txt         # Python dependencies
├── pytest.ini              # Test configuration
└── run_tests.py             # Test runner script
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure all tests pass (`python run_tests.py`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Submit a pull request

### Development Guidelines

- Write tests for all new features
- Follow PEP 8 for Python code
- Use TypeScript for frontend development
- Add docstrings to all functions and classes
- Update documentation for API changes

## License

This project is licensed under the MIT License.