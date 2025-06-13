#!/usr/bin/env python3
"""
Portfolio Tracker API Demo Script

This script demonstrates the complete functionality of the Portfolio Tracker API
including portfolio management, asset tracking, transactions, and performance analysis.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:12000"

def print_response(response, title):
    """Print formatted API response"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(json.dumps(data, indent=2))
        except:
            print(response.text)
    else:
        print(f"Error: {response.text}")

def demo_portfolio_tracker():
    """Demonstrate the Portfolio Tracker API functionality"""
    
    print("🚀 Portfolio Tracker API Demo")
    print("=" * 50)
    
    # 1. Health Check
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "1. Health Check")
    
    # 2. List existing portfolios
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/")
    print_response(response, "2. List Portfolios")
    
    # 3. Create a new portfolio
    portfolio_data = {
        "name": "Demo Portfolio",
        "description": "API demonstration portfolio"
    }
    response = requests.post(f"{BASE_URL}/api/v1/portfolios/", json=portfolio_data)
    print_response(response, "3. Create New Portfolio")
    
    if response.status_code == 200:
        portfolio_id = response.json()["id"]
        
        # 4. List available assets
        response = requests.get(f"{BASE_URL}/api/v1/assets/")
        print_response(response, "4. List Available Assets")
        
        # 5. Create buy transaction for AAPL
        transaction_data = {
            "portfolio_id": portfolio_id,
            "asset_id": 1,  # AAPL
            "transaction_type": "buy",
            "quantity": 15,
            "price": 180.00,
            "total_amount": 2700.00,
            "transaction_date": "2025-06-13T09:00:00Z"
        }
        response = requests.post(f"{BASE_URL}/api/v1/transactions/", json=transaction_data)
        print_response(response, "5. Buy AAPL Shares")
        
        # 6. Create buy transaction for GOOGL
        transaction_data = {
            "portfolio_id": portfolio_id,
            "asset_id": 2,  # GOOGL
            "transaction_type": "buy",
            "quantity": 25,
            "price": 160.00,
            "total_amount": 4000.00,
            "transaction_date": "2025-06-13T09:30:00Z"
        }
        response = requests.post(f"{BASE_URL}/api/v1/transactions/", json=transaction_data)
        print_response(response, "6. Buy GOOGL Shares")
        
        # 7. Create buy transaction for MSFT
        transaction_data = {
            "portfolio_id": portfolio_id,
            "asset_id": 3,  # MSFT
            "transaction_type": "buy",
            "quantity": 20,
            "price": 400.00,
            "total_amount": 8000.00,
            "transaction_date": "2025-06-13T10:00:00Z"
        }
        response = requests.post(f"{BASE_URL}/api/v1/transactions/", json=transaction_data)
        print_response(response, "7. Buy MSFT Shares")
        
        # 8. Get portfolio holdings
        response = requests.get(f"{BASE_URL}/api/v1/holdings/?portfolio_id={portfolio_id}")
        print_response(response, "8. Portfolio Holdings")
        
        # 9. Get portfolio performance
        response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/performance")
        print_response(response, "9. Portfolio Performance Analysis")
        
        # 10. Get portfolio diversification
        response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/diversification")
        print_response(response, "10. Portfolio Diversification Analysis")
        
        # 11. List all transactions for the portfolio
        response = requests.get(f"{BASE_URL}/api/v1/transactions/?portfolio_id={portfolio_id}")
        print_response(response, "11. Portfolio Transactions")
        
        # 12. Update asset prices
        response = requests.post(f"{BASE_URL}/api/v1/assets/update-prices")
        print_response(response, "12. Update Asset Prices")
        
        # 13. Get updated performance after price update
        response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/performance")
        print_response(response, "13. Updated Portfolio Performance")
        
        # 14. Create a sell transaction
        transaction_data = {
            "portfolio_id": portfolio_id,
            "asset_id": 1,  # AAPL
            "transaction_type": "sell",
            "quantity": 5,
            "price": 200.00,
            "total_amount": 1000.00,
            "transaction_date": "2025-06-13T11:00:00Z"
        }
        response = requests.post(f"{BASE_URL}/api/v1/transactions/", json=transaction_data)
        print_response(response, "14. Sell AAPL Shares")
        
        # 15. Final portfolio performance
        response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/performance")
        print_response(response, "15. Final Portfolio Performance")
        
        print(f"\n{'='*50}")
        print("✅ Demo completed successfully!")
        print(f"Portfolio ID: {portfolio_id}")
        print("Check the API documentation at: http://localhost:12000/docs")
        print(f"{'='*50}")

if __name__ == "__main__":
    try:
        demo_portfolio_tracker()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Please make sure the server is running on http://localhost:12000")
        print("Run: python main.py")
    except Exception as e:
        print(f"❌ Error: {e}")