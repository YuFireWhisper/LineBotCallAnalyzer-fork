#!/usr/bin/env python3
"""
Test runner script for the Line Bot Call Analyzer.
"""
import sys
import os
import unittest

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_unit_tests():
    """Run all unit tests."""
    print("Running unit tests...")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/unit', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def run_integration_tests():
    """Run all integration tests."""
    print("Running integration tests...")
    loader = unittest.TestLoader()
    suite = loader.discover('tests/integration', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

def run_all_tests():
    """Run all tests."""
    print("Running all tests...")
    unit_success = run_unit_tests()
    print("\n" + "="*50 + "\n")
    integration_success = run_integration_tests()
    
    if unit_success and integration_success:
        print("\n✅ All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed!")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run tests for Line Bot Call Analyzer")
    parser.add_argument(
        "--type", 
        choices=["unit", "integration", "all"], 
        default="all",
        help="Type of tests to run"
    )
    
    args = parser.parse_args()
    
    success = False
    if args.type == "unit":
        success = run_unit_tests()
    elif args.type == "integration":
        success = run_integration_tests()
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)
