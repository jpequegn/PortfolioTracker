#!/usr/bin/env python3
"""
Test runner script for Portfolio Tracker
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    print(f"Exit code: {result.returncode}")
    return result.returncode == 0


def main():
    """Main test runner"""
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("Portfolio Tracker Test Suite")
    print("=" * 60)
    
    # Check if pytest is available
    if not run_command("python -m pytest --version", "Checking pytest installation"):
        print("ERROR: pytest is not installed. Please install it with: pip install pytest")
        return 1
    
    # Run different test suites
    test_commands = [
        ("python -m pytest tests/unit/ -v", "Unit Tests"),
        ("python -m pytest tests/integration/ -v", "Integration Tests"),
        ("python -m pytest tests/ --cov=app --cov-report=term-missing", "All Tests with Coverage"),
    ]
    
    results = []
    for command, description in test_commands:
        success = run_command(command, description)
        results.append((description, success))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    all_passed = True
    for description, success in results:
        status = "PASSED" if success else "FAILED"
        print(f"{description}: {status}")
        if not success:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())