"""Integration tests (marked for CI)."""

import pytest
from unittest.mock import patch, Mock


@pytest.mark.integration
class TestIntegration:
    """Integration tests that require external services."""

    @pytest.mark.skip(reason="Requires live ClickHouse connection")
    def test_clickhouse_playground_connection(self):
        """Test connection to ClickHouse SQL Playground."""
        from mcp_clickhouse_cloud.mcp_env import ClickHouseConfig
        import os

        # Override config for playground
        with patch.dict(
            os.environ,
            {
                "CLICKHOUSE_HOST": "sql-clickhouse.clickhouse.com",
                "CLICKHOUSE_PORT": "8443",
                "CLICKHOUSE_USER": "demo",
                "CLICKHOUSE_PASSWORD": "",
                "CLICKHOUSE_SECURE": "true",
                "CLICKHOUSE_VERIFY": "true",
            },
        ):
            from mcp_clickhouse_cloud import create_clickhouse_client, run_select_query

            # Test basic connection
            client = create_clickhouse_client()
            assert client is not None

            # Test simple query
            result = run_select_query("SELECT 1 as test_value")
            assert result["status"] == "success"
            assert result["rows"][0][0] == 1

    @pytest.mark.skip(reason="Requires live ClickHouse connection")
    @pytest.mark.slow
    def test_large_query_performance(self, clickhouse_client, test_database):
        """Test performance with larger datasets."""
        from mcp_clickhouse_cloud import run_select_query

        # Create a larger test table
        large_table = "performance_test_table"
        clickhouse_client.command(f"DROP TABLE IF EXISTS {test_database}.{large_table}")

        clickhouse_client.command(
            f"""
            CREATE TABLE {test_database}.{large_table} (
                id UInt32,
                value String
            ) ENGINE = MergeTree()
            ORDER BY id
        """
        )

        # Insert more data
        clickhouse_client.command(
            f"""
            INSERT INTO {test_database}.{large_table} 
            SELECT number, toString(number) 
            FROM numbers(10000)
        """
        )

        # Test query performance
        import time

        start_time = time.time()
        result = run_select_query(f"SELECT COUNT(*) FROM {test_database}.{large_table}")
        end_time = time.time()

        assert result["status"] == "success"
        assert result["rows"][0][0] == 10000
        assert (end_time - start_time) < 5.0  # Should complete within 5 seconds

        # Cleanup
        clickhouse_client.command(f"DROP TABLE {test_database}.{large_table}")
