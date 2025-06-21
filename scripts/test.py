#!/usr/bin/env python3
"""
Test runner script for MCP ClickHouse Cloud.

This script provides a convenient way to run different types of tests
with proper environment setup and reporting.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"🚀 {description}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def check_clickhouse_connection() -> bool:
    """Check if ClickHouse is available."""
    host = os.getenv("CLICKHOUSE_HOST", "localhost")
    port = os.getenv("CLICKHOUSE_PORT", "8123")

    print(f"🔍 Checking ClickHouse connection at {host}:{port}")

    try:
        import requests

        response = requests.get(f"http://{host}:{port}/ping", timeout=5)
        if response.status_code == 200:
            print("✅ ClickHouse is available")
            return True
        else:
            print(f"❌ ClickHouse returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ClickHouse connection failed: {e}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="MCP ClickHouse Cloud Test Runner")
    parser.add_argument(
        "test_type",
        choices=["unit", "integration", "cloud", "all", "coverage", "lint", "format", "type"],
        help="Type of tests to run",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Run tests in verbose mode")
    parser.add_argument(
        "--fast", "-f", action="store_true", help="Run tests in fast mode (exit on first failure)"
    )
    parser.add_argument("--watch", "-w", action="store_true", help="Run tests in watch mode")
    parser.add_argument("--pattern", "-k", help="Run only tests matching this pattern")

    args = parser.parse_args()

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🧪 MCP ClickHouse Cloud Test Runner")
    print(f"📁 Project root: {project_root}")
    print(f"🎯 Test type: {args.test_type}")
    print()

    # Base pytest command
    pytest_cmd = ["uv", "run", "pytest"]

    if args.verbose:
        pytest_cmd.append("-v")

    if args.fast:
        pytest_cmd.append("-x")

    if args.pattern:
        pytest_cmd.extend(["-k", args.pattern])

    success = True

    # Run different test types
    if args.test_type == "lint":
        success &= run_command(["uv", "run", "ruff", "check", "."], "Linting with Ruff")

    elif args.test_type == "format":
        success &= run_command(
            ["uv", "run", "ruff", "format", "--check", "."], "Format checking with Ruff"
        )

    elif args.test_type == "type":
        success &= run_command(
            ["uv", "run", "mypy", "mcp_clickhouse_cloud"], "Type checking with MyPy"
        )

    elif args.test_type == "unit":
        cmd = pytest_cmd + ["-m", "not integration and not slow"]
        if args.watch:
            cmd = ["uv", "run", "pytest-watch", "--runner"] + [" ".join(cmd)]
        success &= run_command(cmd, "Unit tests")

    elif args.test_type == "integration":
        if not check_clickhouse_connection():
            print("❌ ClickHouse not available. Please start ClickHouse:")
            print(
                "   docker run -d --name clickhouse-test -p 8123:8123 clickhouse/clickhouse-server"
            )
            return False

        cmd = pytest_cmd + ["-m", "integration"]
        success &= run_command(cmd, "Integration tests")

    elif args.test_type == "cloud":
        cmd = pytest_cmd + [
            "tests/test_cloud_tools.py",
            "tests/test_configuration.py::TestCloudConfiguration",
        ]
        success &= run_command(cmd, "Cloud API tests")

    elif args.test_type == "coverage":
        cmd = pytest_cmd + [
            "--cov=mcp_clickhouse_cloud",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-branch",
        ]
        success &= run_command(cmd, "Coverage tests")
        if success:
            print("📊 Coverage report generated in htmlcov/index.html")

    elif args.test_type == "all":
        # Run all test types in sequence
        print("🔍 Running comprehensive test suite...")

        # Lint first
        success &= run_command(["uv", "run", "ruff", "check", "."], "Linting")

        # Format check
        success &= run_command(["uv", "run", "ruff", "format", "--check", "."], "Format checking")

        # Type check
        success &= run_command(["uv", "run", "mypy", "mcp_clickhouse_cloud"], "Type checking")

        # Unit tests
        cmd = pytest_cmd + ["-m", "not integration and not slow"]
        success &= run_command(cmd, "Unit tests")

        # Cloud API tests
        cmd = pytest_cmd + ["tests/test_cloud_tools.py"]
        success &= run_command(cmd, "Cloud API tests")

        # Integration tests (if ClickHouse available)
        if check_clickhouse_connection():
            cmd = pytest_cmd + ["-m", "integration"]
            success &= run_command(cmd, "Integration tests")
        else:
            print("⚠️ Skipping integration tests (ClickHouse not available)")

    print()
    if success:
        print("✅ All tests completed successfully!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
