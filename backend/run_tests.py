#!/usr/bin/env python3
"""Test runner script for CV2Interview backend."""

import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {description} failed!")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run CV2Interview backend tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--api", action="store_true", help="Run API tests only")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--lint", action="store_true", help="Run linting checks")
    parser.add_argument("--format", action="store_true", help="Format code")
    parser.add_argument("--all", action="store_true", help="Run all tests and checks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    print(f"Working directory: {backend_dir}")
    
    success = True
    
    # If no specific test type is specified, run all
    if not any([args.unit, args.integration, args.api, args.coverage, args.lint, args.format]):
        args.all = True
    
    # Code formatting
    if args.format or args.all:
        print("\n🔧 Formatting code...")
        commands = [
            (["python", "-m", "black", "app/", "tests/"], "Black code formatting"),
            (["python", "-m", "isort", "app/", "tests/"], "Import sorting"),
        ]
        
        for command, description in commands:
            if not run_command(command, description):
                success = False
    
    # Linting
    if args.lint or args.all:
        print("\n🔍 Running linting checks...")
        commands = [
            (["python", "-m", "flake8", "app/", "tests/"], "Flake8 linting"),
            (["python", "-m", "mypy", "app/"], "MyPy type checking"),
        ]
        
        for command, description in commands:
            if not run_command(command, description):
                print(f"Warning: {description} failed, but continuing...")
    
    # Unit tests
    if args.unit or args.all:
        print("\n🧪 Running unit tests...")
        command = ["python", "-m", "pytest", "tests/test_tools.py", "-m", "unit"]
        if args.verbose:
            command.append("-v")
        
        if not run_command(command, "Unit tests"):
            success = False
    
    # Integration tests
    if args.integration or args.all:
        print("\n🔗 Running integration tests...")
        command = ["python", "-m", "pytest", "tests/test_analytics.py", "-m", "integration"]
        if args.verbose:
            command.append("-v")
        
        if not run_command(command, "Integration tests"):
            success = False
    
    # API tests
    if args.api or args.all:
        print("\n🌐 Running API tests...")
        command = ["python", "-m", "pytest", "tests/test_api.py", "-m", "api"]
        if args.verbose:
            command.append("-v")
        
        if not run_command(command, "API tests"):
            success = False
    
    # All tests with coverage
    if args.coverage or args.all:
        print("\n📊 Running all tests with coverage...")
        command = [
            "python", "-m", "pytest", 
            "tests/",
            "--cov=app",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-fail-under=70"
        ]
        if args.verbose:
            command.append("-v")
        
        if not run_command(command, "Coverage tests"):
            success = False
        else:
            print("\n📈 Coverage report generated in htmlcov/index.html")
    
    # Summary
    print(f"\n{'='*60}")
    if success:
        print("✅ All tests and checks passed!")
        print("\nNext steps:")
        print("1. Review coverage report: htmlcov/index.html")
        print("2. Fix any linting issues if present")
        print("3. Add more tests for uncovered code")
    else:
        print("❌ Some tests or checks failed!")
        print("\nPlease fix the issues and run tests again.")
        sys.exit(1)
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
