#!/usr/bin/env python3
"""Main entry point for the MCP ClickHouse server."""

import sys
import logging
from typing import NoReturn

from .mcp_server import mcp


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def main() -> NoReturn:
    """Start the MCP ClickHouse server.
    
    This function initializes logging and starts the FastMCP server.
    It does not return as the server runs indefinitely.
    """
    try:
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting MCP ClickHouse server...")
        
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()