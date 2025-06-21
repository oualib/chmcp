# Copyright 2025 Badr Ouali
# SPDX-License-Identifier: Apache-2.0

"""Cloud configuration module for ClickHouse Cloud API access.

This module handles authentication and configuration for ClickHouse Cloud API.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ClickHouseCloudConfig:
    """Configuration for ClickHouse Cloud API access.

    Required environment variables:
        CLICKHOUSE_CLOUD_KEY_ID: ClickHouse Cloud API key ID
        CLICKHOUSE_CLOUD_KEY_SECRET: ClickHouse Cloud API key secret

    Optional environment variables:
        CLICKHOUSE_CLOUD_API_URL: API base URL (default: https://api.clickhouse.cloud)
        CLICKHOUSE_CLOUD_TIMEOUT: Request timeout in seconds (default: 30)
        CLICKHOUSE_CLOUD_VERIFY_SSL: Verify SSL certificates (default: true)
    """

    key_id: str
    key_secret: str
    api_url: str
    timeout: int
    verify_ssl: bool = True

    @classmethod
    def from_environment(cls) -> "ClickHouseCloudConfig":
        """Create configuration from environment variables.

        Returns:
            ClickHouseCloudConfig: Configuration instance

        Raises:
            ValueError: If required environment variables are missing
        """
        cls._validate_required_environment_variables()

        return cls(
            key_id=os.environ["CLICKHOUSE_CLOUD_KEY_ID"],
            key_secret=os.environ["CLICKHOUSE_CLOUD_KEY_SECRET"],
            api_url=os.getenv("CLICKHOUSE_CLOUD_API_URL", "https://api.clickhouse.cloud"),
            timeout=cls._parse_int_env("CLICKHOUSE_CLOUD_TIMEOUT", default=30),
            verify_ssl=cls._parse_boolean_env("CLICKHOUSE_CLOUD_VERIFY_SSL", default=True),
        )

    def get_auth_tuple(self) -> tuple[str, str]:
        """Get authentication tuple for requests.

        Returns:
            tuple: (key_id, key_secret) for basic auth
        """
        return (self.key_id, self.key_secret)

    @staticmethod
    def _validate_required_environment_variables() -> None:
        """Validate required environment variables are set.

        Raises:
            ValueError: If required variables are missing
        """
        required_vars = ["CLICKHOUSE_CLOUD_KEY_ID", "CLICKHOUSE_CLOUD_KEY_SECRET"]
        missing_vars = [var for var in required_vars if var not in os.environ]

        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

    @staticmethod
    def _parse_int_env(var_name: str, default: int) -> int:
        """Parse an integer environment variable.

        Args:
            var_name: Environment variable name
            default: Default value if not set

        Returns:
            int: Parsed value

        Raises:
            ValueError: If value cannot be parsed as integer
        """
        value = os.getenv(var_name)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError as e:
            raise ValueError(f"Invalid integer value for {var_name}: {value}") from e

    @staticmethod
    def _parse_boolean_env(var_name: str, default: bool) -> bool:
        """Parse a boolean environment variable.

        Args:
            var_name: Environment variable name
            default: Default value if not set

        Returns:
            bool: Parsed boolean value
        """
        value = os.getenv(var_name)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")


class CloudConfigManager:
    """Singleton manager for ClickHouseCloudConfig."""

    _instance: Optional[ClickHouseCloudConfig] = None

    @classmethod
    def get_config(cls) -> ClickHouseCloudConfig:
        """Get the singleton cloud configuration instance.

        Returns:
            ClickHouseCloudConfig: Configuration instance
        """
        if cls._instance is None:
            cls._instance = ClickHouseCloudConfig.from_environment()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None


def get_cloud_config() -> ClickHouseCloudConfig:
    """Get the singleton cloud configuration instance.

    Returns:
        ClickHouseCloudConfig: Configuration instance
    """
    return CloudConfigManager.get_config()
