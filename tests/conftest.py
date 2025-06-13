"""
Test configuration and fixtures for Portfolio Tracker tests
"""
import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.core.config import Settings
from main import app


@pytest.fixture(scope="session")
def test_settings():
    """Test settings with in-memory database"""
    return Settings(
        database_url="sqlite:///:memory:",
        debug=True,
        secret_key="test-secret-key"
    )


@pytest.fixture(scope="session")
def test_engine(test_settings):
    """Create test database engine"""
    engine = create_engine(
        test_settings.database_url,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="session")
def test_session_factory(test_engine):
    """Create test session factory"""
    return sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture
def test_db(test_session_factory):
    """Create test database session"""
    session = test_session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(test_db):
    """Create test client with test database"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing"""
    return {
        "name": "Test Portfolio",
        "description": "A test portfolio for unit testing"
    }


@pytest.fixture
def sample_asset_data():
    """Sample asset data for testing"""
    return {
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "asset_type": "stock",
        "exchange": "NASDAQ",
        "currency": "USD",
        "current_price": "150.00"
    }


@pytest.fixture
def sample_transaction_data():
    """Sample transaction data for testing"""
    return {
        "transaction_type": "buy",
        "quantity": "10.0",
        "price": "150.00",
        "total_amount": "1500.00",
        "transaction_date": "2024-01-15T10:00:00",
        "notes": "Test transaction"
    }