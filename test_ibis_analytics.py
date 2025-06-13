#!/usr/bin/env python3
"""
Test script for the new ibis-based analytics endpoints
"""

import requests

BASE_URL = "http://localhost:12000"

def test_ibis_analytics():
    """Test the new ibis-based analytics endpoints"""
    print("Testing Ibis Analytics Endpoints...")
    
    # Test health check first
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Get portfolios to find a valid portfolio ID
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/")
    portfolios = response.json()
    if not portfolios:
        print("No portfolios found!")
        return
    
    portfolio_id = portfolios[0]["id"]
    print(f"Testing with portfolio ID: {portfolio_id}")
    
    # Test original performance endpoint (now using ibis)
    print("\n--- Testing Portfolio Performance (ibis-enhanced) ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/performance")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Portfolio Performance: {response.status_code}")
        print(f"  Total Value: ${data.get('total_value', 0)}")
        print(f"  Total Cost: ${data.get('total_cost', 0)}")
        print(f"  Gain/Loss: ${data.get('total_gain_loss', 0)} ({data.get('total_gain_loss_percent', 0)}%)")
        print(f"  Holdings: {len(data.get('holdings', []))}")
    else:
        print(f"✗ Portfolio Performance failed: {response.status_code}")
        print(f"  Error: {response.text}")
    
    # Test original diversification endpoint (now using ibis)
    print("\n--- Testing Portfolio Diversification (ibis-enhanced) ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/diversification")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Portfolio Diversification: {response.status_code}")
        print(f"  Total Value: ${data.get('total_value', 0)}")
        print(f"  Asset Types: {list(data.get('by_asset_type', {}).keys())}")
        print(f"  Individual Assets: {len(data.get('by_asset', []))}")
    else:
        print(f"✗ Portfolio Diversification failed: {response.status_code}")
        print(f"  Error: {response.text}")
    
    # Test new advanced performance metrics endpoint
    print("\n--- Testing Advanced Performance Metrics (new ibis endpoint) ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/analytics/performance")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Advanced Performance Metrics: {response.status_code}")
        print(f"  Total Positions: {data.get('total_positions', 0)}")
        print(f"  Market Value: ${data.get('total_market_value', 0)}")
        print(f"  Cost Basis: ${data.get('total_cost_basis', 0)}")
        print(f"  Unrealized Gain/Loss: ${data.get('unrealized_gain_loss', 0)} ({data.get('unrealized_gain_loss_percent', 0)}%)")
        price_stats = data.get('price_statistics', {})
        print(f"  Price Range: ${price_stats.get('min_price', 0)} - ${price_stats.get('max_price', 0)} (avg: ${price_stats.get('avg_price', 0)})")
    else:
        print(f"✗ Advanced Performance Metrics failed: {response.status_code}")
        print(f"  Error: {response.text}")
    
    # Test new asset allocation analysis endpoint
    print("\n--- Testing Asset Allocation Analysis (new ibis endpoint) ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/analytics/allocation")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Asset Allocation Analysis: {response.status_code}")
        print(f"  Total Value: ${data.get('total_value', 0)}")
        
        by_asset_type = data.get('by_asset_type', {})
        print(f"  By Asset Type:")
        for asset_type, info in by_asset_type.items():
            print(f"    {asset_type}: ${info.get('value', 0)} ({info.get('percentage', 0):.2f}%)")
        
        # Note: Sector analysis not available as sector column doesn't exist in current schema
        
        by_currency = data.get('by_currency', {})
        print(f"  By Currency:")
        for currency, info in by_currency.items():
            print(f"    {currency}: ${info.get('value', 0)} ({info.get('percentage', 0):.2f}%)")
    else:
        print(f"✗ Asset Allocation Analysis failed: {response.status_code}")
        print(f"  Error: {response.text}")
    
    print("\nIbis analytics tests completed!")

if __name__ == "__main__":
    test_ibis_analytics()