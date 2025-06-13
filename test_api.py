#!/usr/bin/env python3
"""
Simple test script to verify the API is working
"""
import requests
import json

BASE_URL = "http://localhost:12000/api/v1"


def test_api():
    print("Testing Portfolio Tracker API...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:12000/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        
        # Test getting portfolios
        response = requests.get(f"{BASE_URL}/portfolios/")
        print(f"Get portfolios: {response.status_code}")
        if response.status_code == 200:
            portfolios = response.json()
            print(f"Found {len(portfolios)} portfolios")
            
            if portfolios:
                # Test getting portfolio performance
                portfolio_id = portfolios[0]['id']
                response = requests.get(f"{BASE_URL}/portfolios/{portfolio_id}/performance")
                print(f"Portfolio performance: {response.status_code}")
                if response.status_code == 200:
                    performance = response.json()
                    print(f"Portfolio value: ${performance.get('total_value', 0)}")
        
        # Test getting assets
        response = requests.get(f"{BASE_URL}/assets/")
        print(f"Get assets: {response.status_code}")
        if response.status_code == 200:
            assets = response.json()
            print(f"Found {len(assets)} assets")
        
        # Test asset lookup
        response = requests.get(f"{BASE_URL}/assets/lookup/AAPL")
        print(f"Asset lookup AAPL: {response.status_code}")
        if response.status_code == 200:
            asset_info = response.json()
            print(f"AAPL info: {asset_info.get('name', 'Unknown')}")
        
        print("API tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Make sure the server is running on port 12000")
    except Exception as e:
        print(f"Error testing API: {e}")


if __name__ == "__main__":
    test_api()