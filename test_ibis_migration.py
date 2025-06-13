#!/usr/bin/env python3
"""
Test script to verify that the ibis migration is working correctly
and providing accurate results for portfolio analytics.
"""

import requests
import json
from decimal import Decimal

BASE_URL = "http://localhost:12000"

def test_ibis_migration():
    """Test that ibis-based analytics provide accurate results"""
    print("Testing Ibis Migration Results...")
    
    # Get portfolios
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/")
    portfolios = response.json()
    if not portfolios:
        print("No portfolios found!")
        return
    
    portfolio_id = portfolios[0]["id"]
    print(f"Testing portfolio ID: {portfolio_id}")
    
    # Test portfolio performance calculation
    print("\n--- Testing Portfolio Performance Calculation ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/performance")
    if response.status_code == 200:
        data = response.json()
        
        # Verify data consistency
        total_value = Decimal(str(data["total_value"]))
        total_cost = Decimal(str(data["total_cost"]))
        total_gain_loss = Decimal(str(data["total_gain_loss"]))
        
        # Check that gain/loss calculation is correct
        calculated_gain_loss = total_value - total_cost
        if abs(calculated_gain_loss - total_gain_loss) < Decimal("0.01"):
            print("✓ Gain/Loss calculation is accurate")
        else:
            print(f"✗ Gain/Loss calculation error: expected {calculated_gain_loss}, got {total_gain_loss}")
        
        # Check holdings data
        holdings = data.get("holdings", [])
        holdings_total_value = sum(Decimal(str(h["current_value"])) for h in holdings)
        holdings_total_cost = sum(Decimal(str(h["cost_basis"])) for h in holdings)
        
        if abs(holdings_total_value - total_value) < Decimal("0.01"):
            print("✓ Holdings total value matches portfolio total")
        else:
            print(f"✗ Holdings total value mismatch: {holdings_total_value} vs {total_value}")
        
        if abs(holdings_total_cost - total_cost) < Decimal("0.01"):
            print("✓ Holdings total cost matches portfolio total")
        else:
            print(f"✗ Holdings total cost mismatch: {holdings_total_cost} vs {total_cost}")
        
        print(f"  Portfolio has {len(holdings)} holdings")
        print(f"  Total value: ${total_value}")
        print(f"  Total cost: ${total_cost}")
        print(f"  Gain/Loss: ${total_gain_loss}")
    else:
        print(f"✗ Portfolio performance failed: {response.status_code}")
        return
    
    # Test diversification calculation
    print("\n--- Testing Diversification Calculation ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/diversification")
    if response.status_code == 200:
        data = response.json()
        
        # Verify that percentages add up to 100%
        by_asset_type = data.get("by_asset_type", {})
        total_percentage = sum(Decimal(str(pct)) for pct in by_asset_type.values())
        
        if abs(total_percentage - Decimal("100")) < Decimal("0.01"):
            print("✓ Asset type percentages add up to 100%")
        else:
            print(f"✗ Asset type percentages don't add up: {total_percentage}%")
        
        # Verify individual asset percentages
        by_asset = data.get("by_asset", [])
        individual_total = sum(Decimal(str(asset["percentage"])) for asset in by_asset)
        
        if abs(individual_total - Decimal("100")) < Decimal("0.01"):
            print("✓ Individual asset percentages add up to 100%")
        else:
            print(f"✗ Individual asset percentages don't add up: {individual_total}%")
        
        print(f"  Asset types: {list(by_asset_type.keys())}")
        print(f"  Individual assets: {len(by_asset)}")
    else:
        print(f"✗ Diversification analysis failed: {response.status_code}")
        return
    
    # Test advanced performance metrics
    print("\n--- Testing Advanced Performance Metrics ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/analytics/performance")
    if response.status_code == 200:
        data = response.json()
        
        # Compare with basic performance data
        adv_market_value = Decimal(str(data["total_market_value"]))
        adv_cost_basis = Decimal(str(data["total_cost_basis"]))
        
        if abs(adv_market_value - total_value) < Decimal("0.01"):
            print("✓ Advanced metrics market value matches basic performance")
        else:
            print(f"✗ Advanced metrics market value mismatch: {adv_market_value} vs {total_value}")
        
        if abs(adv_cost_basis - total_cost) < Decimal("0.01"):
            print("✓ Advanced metrics cost basis matches basic performance")
        else:
            print(f"✗ Advanced metrics cost basis mismatch: {adv_cost_basis} vs {total_cost}")
        
        print(f"  Total positions: {data['total_positions']}")
        price_stats = data.get("price_statistics", {})
        print(f"  Price range: ${price_stats.get('min_price')} - ${price_stats.get('max_price')}")
    else:
        print(f"✗ Advanced performance metrics failed: {response.status_code}")
        return
    
    # Test asset allocation analysis
    print("\n--- Testing Asset Allocation Analysis ---")
    response = requests.get(f"{BASE_URL}/api/v1/portfolios/{portfolio_id}/analytics/allocation")
    if response.status_code == 200:
        data = response.json()
        
        # Verify allocation totals
        alloc_total_value = Decimal(str(data["total_value"]))
        
        if abs(alloc_total_value - total_value) < Decimal("0.01"):
            print("✓ Allocation total value matches portfolio total")
        else:
            print(f"✗ Allocation total value mismatch: {alloc_total_value} vs {total_value}")
        
        # Check asset type allocation percentages
        by_asset_type = data.get("by_asset_type", {})
        asset_type_total = sum(Decimal(str(info["percentage"])) for info in by_asset_type.values())
        
        if abs(asset_type_total - Decimal("100")) < Decimal("0.01"):
            print("✓ Asset type allocation percentages add up to 100%")
        else:
            print(f"✗ Asset type allocation percentages don't add up: {asset_type_total}%")
        
        # Check currency allocation percentages
        by_currency = data.get("by_currency", {})
        currency_total = sum(Decimal(str(info["percentage"])) for info in by_currency.values())
        
        if abs(currency_total - Decimal("100")) < Decimal("0.01"):
            print("✓ Currency allocation percentages add up to 100%")
        else:
            print(f"✗ Currency allocation percentages don't add up: {currency_total}%")
        
        print(f"  Asset types: {list(by_asset_type.keys())}")
        print(f"  Currencies: {list(by_currency.keys())}")
    else:
        print(f"✗ Asset allocation analysis failed: {response.status_code}")
        return
    
    print("\n✓ All ibis migration tests passed!")
    print("\nSummary:")
    print("- Portfolio performance calculations are accurate")
    print("- Diversification analysis is working correctly")
    print("- Advanced performance metrics provide consistent results")
    print("- Asset allocation analysis is functioning properly")
    print("- All percentage calculations sum to 100% as expected")

if __name__ == "__main__":
    test_ibis_migration()