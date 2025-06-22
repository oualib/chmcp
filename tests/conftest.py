"""Test configuration and fixtures."""

import os
import pytest
from unittest.mock import Mock, patch
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()


@pytest.fixture(scope="session")
def clickhouse_config():
    """Provide test ClickHouse configuration."""
    return {
        "host": os.getenv("CLICKHOUSE_HOST", "localhost"),
        "port": int(os.getenv("CLICKHOUSE_PORT", "8123")),
        "user": os.getenv("CLICKHOUSE_USER", "default"),
        "password": os.getenv("CLICKHOUSE_PASSWORD", ""),
        "secure": os.getenv("CLICKHOUSE_SECURE", "false").lower() == "true",
        "verify": os.getenv("CLICKHOUSE_VERIFY", "false").lower() == "true",
    }


@pytest.fixture(scope="session")
def test_database():
    """Provide test database name."""
    return "test_chmcp"


@pytest.fixture(scope="session")
def test_table():
    """Provide test table name."""
    return "test_table"


@pytest.fixture(scope="session")
def clickhouse_client(clickhouse_config, test_database, test_table):
    """Create a ClickHouse client and set up test data."""
    from chmcp import create_clickhouse_client

    try:
        client = create_clickhouse_client()

        # Create test database
        client.command(f"CREATE DATABASE IF NOT EXISTS {test_database}")

        # Drop table if exists
        client.command(f"DROP TABLE IF EXISTS {test_database}.{test_table}")

        # Create test table with comprehensive schema
        client.command(
            f"""
            CREATE TABLE {test_database}.{test_table} (
                id UInt32 COMMENT 'Primary identifier',
                name String COMMENT 'User name field',
                email String COMMENT 'Email address',
                age UInt8 COMMENT 'User age',
                created_at DateTime DEFAULT now() COMMENT 'Creation timestamp',
                is_active Boolean DEFAULT true COMMENT 'Active status'
            ) ENGINE = MergeTree()
            ORDER BY id
            COMMENT 'Test table for comprehensive unit testing'
        """
        )

        # Insert test data
        client.command(
            f"""
            INSERT INTO {test_database}.{test_table} 
            (id, name, email, age, is_active) VALUES 
            (1, 'Alice Johnson', 'alice@example.com', 28, true),
            (2, 'Bob Smith', 'bob@example.com', 35, true),
            (3, 'Charlie Brown', 'charlie@example.com', 42, false),
            (4, 'Diana Prince', 'diana@example.com', 30, true)
        """
        )

        yield client

    finally:
        # Cleanup
        try:
            client.command(f"DROP DATABASE IF EXISTS {test_database}")
        except:
            pass


@pytest.fixture
def mock_cloud_client():
    """Mock cloud client for testing cloud functionality."""
    with patch("chmcp.cloud_tools.create_cloud_client") as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client
