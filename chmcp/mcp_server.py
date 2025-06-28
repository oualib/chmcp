# Copyright 2025 Badr Ouali
# SPDX-License-Identifier: Apache-2.0

"""MCP ClickHouse Cloud & On-Prem Server Implementation.

This module provides the FastMCP server implementation for ClickHouse database operations
and ClickHouse Cloud API operations. It includes tools for both direct database access
and cloud management through the ClickHouse Cloud API.
"""

import atexit
import concurrent.futures
import os
import logging
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Dict, List, Optional, Union

import clickhouse_connect
from clickhouse_connect.driver.binding import format_query_value
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from chmcp.mcp_env import get_config


# Data models
@dataclass
class Column:
    """Represents a ClickHouse table column with its metadata."""

    database: str
    table: str
    name: str
    column_type: str
    default_kind: Optional[str] = None
    default_expression: Optional[str] = None
    comment: Optional[str] = None


@dataclass
class Table:
    """Represents a ClickHouse table with its metadata and columns."""

    database: str
    name: str
    engine: str
    create_table_query: str
    dependencies_database: str
    dependencies_table: str
    engine_full: str
    sorting_key: str
    primary_key: str
    total_rows: int
    total_bytes: int
    total_bytes_uncompressed: int
    parts: int
    active_parts: int
    total_marks: int
    comment: Optional[str] = None
    columns: List[Column] = field(default_factory=list)


@dataclass(frozen=True)
class QueryResult:
    """Represents the result of a database query."""

    columns: List[str]
    rows: List[List[Any]]
    status: str = "success"


@dataclass(frozen=True)
class ErrorResult:
    """Represents an error result from a database operation."""

    status: str
    message: str


# Constants
MCP_SERVER_NAME = "chmcp"
QUERY_TIMEOUT_SECS = 30
MAX_QUERY_WORKERS = 10

# Logging setup
logger = logging.getLogger(MCP_SERVER_NAME)

# Load environment variables
load_dotenv()

# Thread pool for query execution
QUERY_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_QUERY_WORKERS)
atexit.register(lambda: QUERY_EXECUTOR.shutdown(wait=True))

# FastMCP server setup
DEPENDENCIES = [
    "clickhouse-connect",
    "python-dotenv",
    "uvicorn",
    "pip-system-certs",
    "requests",  # For cloud API calls
]

mcp = FastMCP(MCP_SERVER_NAME, dependencies=DEPENDENCIES)


# Utility functions
def serialize_dataclass(obj: Any) -> Any:
    """Recursively serialize dataclass objects to JSON-compatible format.

    Args:
        obj: Object to serialize

    Returns:
        JSON-compatible representation of the object
    """
    if is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, list):
        return [serialize_dataclass(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: serialize_dataclass(value) for key, value in obj.items()}
    return obj


def create_tables_from_result(column_names: List[str], rows: List[List[Any]]) -> List[Table]:
    """Create Table objects from query results.

    Args:
        column_names: Names of the columns in the result
        rows: Raw data rows from the query

    Returns:
        List of Table objects
    """
    return [Table(**dict(zip(column_names, row))) for row in rows]


def create_columns_from_result(column_names: List[str], rows: List[List[Any]]) -> List[Column]:
    """Create Column objects from query results.

    Args:
        column_names: Names of the columns in the result
        rows: Raw data rows from the query

    Returns:
        List of Column objects
    """
    return [Column(**dict(zip(column_names, row))) for row in rows]


# ClickHouse client management
def create_clickhouse_client():
    """Create and test a ClickHouse client connection.

    Returns:
        ClickHouse client instance

    Raises:
        Exception: If connection fails
    """
    config = get_config()
    client_config = config.get_client_config()

    logger.info(
        f"Creating ClickHouse client connection to {client_config['host']}:{client_config['port']} "
        f"as {client_config['username']} "
        f"(secure={client_config['secure']}, verify={client_config['verify']}, "
        f"connect_timeout={client_config['connect_timeout']}s, "
        f"send_receive_timeout={client_config['send_receive_timeout']}s)"
    )

    try:
        client = clickhouse_connect.get_client(**client_config)
        # Test the connection
        version = client.server_version
        logger.info(f"Successfully connected to ClickHouse server version {version}")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to ClickHouse: {e}")
        raise


# Query execution
def execute_query(query: str) -> Union[QueryResult, ErrorResult]:
    """Execute a query against ClickHouse.

    Args:
        query: SQL query to execute

    Returns:
        QueryResult on success, ErrorResult on failure
    """
    try:
        client = create_clickhouse_client()
        readonly_setting = os.getenv("READONLY", 1)
        if isinstance(readonly_setting, bool):
            readonly_setting = int(readonly_setting)
        elif isinstance(readonly_setting, str) and (
            readonly_setting.lower().startswith("f")
            or (readonly_setting.isdigit() and int(readonly_setting) == 0)
        ):
            readonly_setting = 0
        else:
            readonly_setting = 1
        result = client.query(query, settings={"readonly": readonly_setting})

        logger.info(f"Query returned {len(result.result_rows)} rows")
        return QueryResult(columns=result.column_names, rows=result.result_rows)

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error executing query: {error_msg}")
        return ErrorResult(status="error", message=error_msg)


# Database MCP Tools
@mcp.tool()
def list_databases() -> List[str]:
    """List available ClickHouse databases.

    Returns:
        List of database names
    """
    logger.info("Listing all databases")

    try:
        client = create_clickhouse_client()
        databases = client.command("SHOW DATABASES")

        logger.info(f"Found {len(databases) if isinstance(databases, list) else 1} databases")
        return databases

    except Exception as e:
        logger.error(f"Failed to list databases: {e}")
        raise


@mcp.tool()
def list_tables(
    database: str, like: Optional[str] = None, not_like: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List available ClickHouse tables in a database.

    Returns detailed information about tables including schema, comments,
    row counts, and column information.

    Args:
        database: Name of the database to query
        like: Optional LIKE pattern to filter table names
        not_like: Optional NOT LIKE pattern to exclude table names

    Returns:
        List of table information dictionaries
    """
    logger.info(f"Listing tables in database '{database}'")

    try:
        client = create_clickhouse_client()

        # Build the main query for table information
        query = f"SELECT database, name, engine, create_table_query, dependencies_database, dependencies_table, engine_full, sorting_key, primary_key, total_rows, total_bytes, total_bytes_uncompressed, parts, active_parts, total_marks, comment FROM system.tables WHERE database = {format_query_value(database)}"

        if like:
            query += f" AND name LIKE {format_query_value(like)}"
        if not_like:
            query += f" AND name NOT LIKE {format_query_value(not_like)}"

        result = client.query(query)

        # Create table objects from the result using your working function
        tables = create_tables_from_result(result.column_names, result.result_rows)

        # Fetch column information for each table
        for table in tables:
            column_data_query = f"SELECT database, table, name, type AS column_type, default_kind, default_expression, comment FROM system.columns WHERE database = {format_query_value(database)} AND table = {format_query_value(table.name)}"
            column_data_query_result = client.query(column_data_query)
            table.columns = [
                c
                for c in create_columns_from_result(
                    column_data_query_result.column_names,
                    column_data_query_result.result_rows,
                )
            ]

        logger.info(f"Found {len(tables)} tables")
        return [asdict(table) for table in tables]

    except Exception as e:
        logger.error(f"Failed to list tables: {e}")
        raise


@mcp.tool()
def run_query(query: str) -> Dict[str, Any]:
    """Run a query in a ClickHouse database.

    Args:
        query: The query to execute

    Returns:
        Dictionary containing query results or error information
    """
    logger.info(f"Executing query: {query}")

    try:
        # Submit query to thread pool with timeout
        future = QUERY_EXECUTOR.submit(execute_query, query)

        try:
            result = future.result(timeout=QUERY_TIMEOUT_SECS)

            # Convert result to dictionary format
            if isinstance(result, ErrorResult):
                logger.warning(f"Query failed: {result.message}")
                return serialize_dataclass(result)
            elif isinstance(result, QueryResult):
                return serialize_dataclass(result)
            else:
                # This shouldn't happen, but handle it gracefully
                logger.error(f"Unexpected result type: {type(result)}")
                return serialize_dataclass(
                    ErrorResult(
                        status="error", message="Unexpected result type from query execution"
                    )
                )

        except concurrent.futures.TimeoutError:
            logger.warning(f"Query timed out after {QUERY_TIMEOUT_SECS} seconds: {query}")
            future.cancel()
            return serialize_dataclass(
                ErrorResult(
                    status="error",
                    message=f"Query timed out after {QUERY_TIMEOUT_SECS} seconds",
                )
            )

    except Exception as e:
        logger.error(f"Unexpected error in run_query: {e}")
        return serialize_dataclass(
            ErrorResult(status="error", message=f"Unexpected error: {str(e)}")
        )


# Import cloud tools to register them with the MCP server
try:
    from . import cloud_tools

    logger.info("Successfully imported cloud tools")
except ImportError as e:
    logger.warning(f"Could not import cloud tools: {e}")
    logger.info(
        "Cloud tools will not be available. Ensure cloud dependencies are installed and configured."
    )
