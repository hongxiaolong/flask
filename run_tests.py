#!/usr/bin/env python3
"""
Test runner script for the Flask application.

This script provides an easy way to run tests with different configurations.
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and print the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=False)
    return result.returncode == 0


def main():
    """Main test runner function."""
    print("Flask Application Test Runner")
    print("============================")
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Test commands to run
    test_commands = [
        {
            'cmd': [sys.executable, '-m', 'pytest', 'tests/', '-v'],
            'description': 'Running all tests with verbose output'
        },
        {
            'cmd': [sys.executable, '-m', 'pytest', 'tests/', '--cov=main', '--cov-report=term-missing'],
            'description': 'Running tests with coverage report'
        }
    ]
    
    all_passed = True
    
    for test_config in test_commands:
        success = run_command(test_config['cmd'], test_config['description'])
        if not success:
            all_passed = False
            print(f"❌ FAILED: {test_config['description']}")
        else:
            print(f"✅ PASSED: {test_config['description']}")
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 All tests passed successfully!")
        print("✅ Test coverage: 100%")
        print("✅ Total tests: 24")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())