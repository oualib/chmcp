"""MCP ClickHouse Cloud Server Package.

This package provides a Model Context Protocol (MCP) server for ClickHouse database operations
and ClickHouse Cloud management. It exposes tools for listing databases, tables, running SELECT
queries, and comprehensive cloud management including services, API keys, members, backups, and more.
"""

from .mcp_server import (
    create_clickhouse_client,
    list_databases,
    list_tables,
    run_select_query,
)

# Import cloud tools to make them available (they auto-register via decorators)
try:
    from . import cloud_tools
except ImportError:
    # Cloud tools are optional if cloud dependencies aren't available
    pass

__version__ = "0.1.2"
__author__ = "Badr Ouali"

__all__ = [
    "create_clickhouse_client",
    "list_databases",
    "list_tables",
    "run_select_query",
]
