"""Tests for configuration management."""

import pytest
import os
from unittest.mock import patch
from chmcp.mcp_env import ClickHouseConfig, ConfigManager
from chmcp.cloud_config import ClickHouseCloudConfig


class TestDatabaseConfiguration:
    """Test database configuration management."""

    def test_clickhouse_config_from_environment(self):
        """Test configuration creation from environment variables."""
        env_vars = {
            "CLICKHOUSE_HOST": "localhost",
            "CLICKHOUSE_USER": "default",
            "CLICKHOUSE_PASSWORD": "",
            "CLICKHOUSE_PORT": "8123",
            "CLICKHOUSE_SECURE": "true",
        }

        with patch.dict(os.environ, env_vars):
            config = ClickHouseConfig.from_environment()

            assert config.host == "localhost"
            assert config.username == "default"
            assert config.password == ""
            assert config.port == 8123
            assert config.secure is True

    def test_clickhouse_config_missing_required_vars(self):
        """Test configuration fails with missing required variables."""
        # Clear required environment variables
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Missing required environment variables"):
                ClickHouseConfig.from_environment()

    def test_clickhouse_config_defaults(self):
        """Test configuration uses correct defaults."""
        env_vars = {
            "CLICKHOUSE_HOST": "localhost",
            "CLICKHOUSE_USER": "default",
            "CLICKHOUSE_PASSWORD": "",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = ClickHouseConfig.from_environment()

            assert config.port == 8443  # Default for secure=True
            assert config.secure is True
            assert config.verify is True
            assert config.connect_timeout == 30
            assert config.send_receive_timeout == 300
            assert config.database is None

    def test_clickhouse_config_port_defaults(self):
        """Test port defaults based on secure setting."""
        # Test secure=False gives port 8123
        env_vars = {
            "CLICKHOUSE_HOST": "localhost",
            "CLICKHOUSE_USER": "default",
            "CLICKHOUSE_PASSWORD": "",
            "CLICKHOUSE_SECURE": "false",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = ClickHouseConfig.from_environment()
            assert config.port == 8123

    def test_config_manager_singleton(self):
        """Test ConfigManager singleton behavior."""
        # Reset singleton
        ConfigManager.reset()

        env_vars = {
            "CLICKHOUSE_HOST": "localhost",
            "CLICKHOUSE_USER": "default",
            "CLICKHOUSE_PASSWORD": "",
        }

        with patch.dict(os.environ, env_vars):
            config1 = ConfigManager.get_config()
            config2 = ConfigManager.get_config()

            # Should be the same instance
            assert config1 is config2


class TestCloudConfiguration:
    """Test cloud configuration management."""

    def test_cloud_config_from_environment(self):
        """Test cloud configuration creation."""
        env_vars = {
            "CLICKHOUSE_CLOUD_KEY_ID": "test-key-id",
            "CLICKHOUSE_CLOUD_KEY_SECRET": "test-key-secret",
            "CLICKHOUSE_CLOUD_API_URL": "https://test-api.clickhouse.com",
            "CLICKHOUSE_CLOUD_TIMEOUT": "60",
        }

        with patch.dict(os.environ, env_vars):
            config = ClickHouseCloudConfig.from_environment()

            assert config.key_id == "test-key-id"
            assert config.key_secret == "test-key-secret"
            assert config.api_url == "https://test-api.clickhouse.com"
            assert config.timeout == 60

    def test_cloud_config_defaults(self):
        """Test cloud configuration defaults."""
        env_vars = {
            "CLICKHOUSE_CLOUD_KEY_ID": "test-key-id",
            "CLICKHOUSE_CLOUD_KEY_SECRET": "test-key-secret",
        }

        with patch.dict(os.environ, env_vars, clear=True):
            config = ClickHouseCloudConfig.from_environment()

            assert config.api_url == "https://api.clickhouse.cloud"
            assert config.timeout == 30

    def test_cloud_config_auth_tuple(self):
        """Test auth tuple generation."""
        env_vars = {
            "CLICKHOUSE_CLOUD_KEY_ID": "test-key-id",
            "CLICKHOUSE_CLOUD_KEY_SECRET": "test-key-secret",
        }

        with patch.dict(os.environ, env_vars):
            config = ClickHouseCloudConfig.from_environment()
            auth_tuple = config.get_auth_tuple()

            assert auth_tuple == ("test-key-id", "test-key-secret")
