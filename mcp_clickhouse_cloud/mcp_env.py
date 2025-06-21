# Copyright 2025 Badr Ouali
# SPDX-License-Identifier: Apache-2.0

"""Environment configuration for the MCP ClickHouse Cloud server.

This module handles all environment variable configuration with sensible defaults
and type conversion using a singleton pattern for efficient configuration access.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ClickHouseConfig:
    """Immutable configuration for ClickHouse connection settings.

    This class handles all environment variable configuration with sensible defaults
    and type conversion. It provides typed properties for accessing each configuration value.

    Required environment variables:
        CLICKHOUSE_HOST: The hostname of the ClickHouse server
        CLICKHOUSE_USER: The username for authentication
        CLICKHOUSE_PASSWORD: The password for authentication

    Optional environment variables (with defaults):
        CLICKHOUSE_PORT: The port number (default: 8443 if secure=True, 8123 if secure=False)
        CLICKHOUSE_SECURE: Enable HTTPS (default: true)
        CLICKHOUSE_VERIFY: Verify SSL certificates (default: true)
        CLICKHOUSE_CONNECT_TIMEOUT: Connection timeout in seconds (default: 30)
        CLICKHOUSE_SEND_RECEIVE_TIMEOUT: Send/receive timeout in seconds (default: 300)
        CLICKHOUSE_DATABASE: Default database to use (default: None)
        CLICKHOUSE_PROXY_PATH: Path for servers behind an HTTP proxy (default: None)
    """

    host: str
    username: str
    password: str
    port: int
    database: Optional[str]
    secure: bool
    verify: bool
    connect_timeout: int
    send_receive_timeout: int
    proxy_path: Optional[str]

    @classmethod
    def from_environment(cls) -> "ClickHouseConfig":
        """Create a ClickHouseConfig instance from environment variables.

        Returns:
            ClickHouseConfig: Configuration instance populated from environment.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        cls._validate_required_environment_variables()

        # Parse secure setting first as it affects port default
        secure = cls._parse_boolean_env("CLICKHOUSE_SECURE", default=True)

        return cls(
            host=os.environ["CLICKHOUSE_HOST"],
            username=os.environ["CLICKHOUSE_USER"],
            password=os.environ["CLICKHOUSE_PASSWORD"],
            port=cls._parse_port(secure),
            database=os.getenv("CLICKHOUSE_DATABASE"),
            secure=secure,
            verify=cls._parse_boolean_env("CLICKHOUSE_VERIFY", default=True),
            connect_timeout=cls._parse_int_env("CLICKHOUSE_CONNECT_TIMEOUT", default=30),
            send_receive_timeout=cls._parse_int_env("CLICKHOUSE_SEND_RECEIVE_TIMEOUT", default=300),
            proxy_path=os.getenv("CLICKHOUSE_PROXY_PATH"),
        )

    def get_client_config(self) -> Dict[str, any]:
        """Get the configuration dictionary for clickhouse_connect client.

        Returns:
            Dict[str, any]: Configuration ready to be passed to clickhouse_connect.get_client()
        """
        config = {
            "host": self.host,
            "port": self.port,
            "username": self.username,
            "password": self.password,
            "secure": self.secure,
            "verify": self.verify,
            "connect_timeout": self.connect_timeout,
            "send_receive_timeout": self.send_receive_timeout,
            "client_name": "mcp_clickhouse_cloud",
        }

        # Add optional fields if they are set
        if self.database:
            config["database"] = self.database

        if self.proxy_path:
            config["proxy_path"] = self.proxy_path

        return config

    @staticmethod
    def _validate_required_environment_variables() -> None:
        """Validate that all required environment variables are set.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        required_vars = ["CLICKHOUSE_HOST", "CLICKHOUSE_USER", "CLICKHOUSE_PASSWORD"]
        missing_vars = [var for var in required_vars if var not in os.environ]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @staticmethod
    def _parse_boolean_env(var_name: str, default: bool) -> bool:
        """Parse a boolean environment variable.

        Args:
            var_name: Name of the environment variable
            default: Default value if not set

        Returns:
            bool: Parsed boolean value
        """
        value = os.getenv(var_name)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def _parse_int_env(var_name: str, default: int) -> int:
        """Parse an integer environment variable.

        Args:
            var_name: Name of the environment variable
            default: Default value if not set

        Returns:
            int: Parsed integer value

        Raises:
            ValueError: If the environment variable cannot be parsed as an integer
        """
        value = os.getenv(var_name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError as e:
            raise ValueError(f"Invalid integer value for {var_name}: {value}") from e

    @staticmethod
    def _parse_port(secure: bool) -> int:
        """Parse the port from environment or return appropriate default.

        Args:
            secure: Whether secure connection is enabled

        Returns:
            int: Port number to use
        """
        port_str = os.getenv("CLICKHOUSE_PORT")
        if port_str is not None:
            try:
                return int(port_str)
            except ValueError as e:
                raise ValueError(f"Invalid port value: {port_str}") from e

        # Return default based on security setting
        return 8443 if secure else 8123


class ConfigManager:
    """Singleton manager for ClickHouseConfig instances."""

    _instance: Optional[ClickHouseConfig] = None

    @classmethod
    def get_config(cls) -> ClickHouseConfig:
        """Get the singleton instance of ClickHouseConfig.

        Returns:
            ClickHouseConfig: The configuration instance
        """
        if cls._instance is None:
            cls._instance = ClickHouseConfig.from_environment()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None


def get_config() -> ClickHouseConfig:
    """Get the singleton instance of ClickHouseConfig.

    This is the main entry point for accessing configuration.

    Returns:
        ClickHouseConfig: The configuration instance
    """
    return ConfigManager.get_config()
