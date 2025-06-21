"""Tests for ClickHouse Cloud API tools."""

import pytest
from unittest.mock import Mock, patch
from mcp_clickhouse_cloud.cloud_client import CloudAPIResponse, CloudAPIError


class TestCloudTools:
    """Test suite for ClickHouse Cloud API tools."""

    def test_cloud_list_organizations_success(self, mock_cloud_client):
        """Test successful organization listing."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_list_organizations

        # Mock successful response
        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-request-123",
            result=[{"id": "org-123", "name": "Test Organization"}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_organizations()

        assert result["status"] == "success"
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["name"] == "Test Organization"
        mock_cloud_client.get.assert_called_once_with("/v1/organizations")

    def test_cloud_list_organizations_error(self, mock_cloud_client):
        """Test organization listing with API error."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_list_organizations

        # Mock error response
        mock_error = CloudAPIError(status=401, error="Unauthorized", request_id="test-request-456")
        mock_cloud_client.get.return_value = mock_error

        result = cloud_list_organizations()

        assert result["status"] == "error"
        assert result["error"] == "Unauthorized"
        assert result["status_code"] == 401

    def test_cloud_get_organization(self, mock_cloud_client):
        """Test getting specific organization details."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_get_organization

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-request-789",
            result={"id": "org-123", "name": "Test Org", "tier": "ENTERPRISE"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_organization("org-123")

        assert result["status"] == "success"
        assert result["data"]["tier"] == "ENTERPRISE"
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123")

    def test_cloud_list_services(self, mock_cloud_client):
        """Test listing services in an organization."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_list_services

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-request-services",
            result=[
                {
                    "id": "service-123",
                    "name": "prod-service",
                    "state": "running",
                    "provider": "aws",
                    "region": "us-east-1",
                }
            ],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_services("org-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["state"] == "running"
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123/services")

    def test_cloud_create_service(self, mock_cloud_client):
        """Test creating a new service."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_create_service

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-service",
            result={
                "service": {"id": "service-new", "name": "test-service", "state": "provisioning"},
                "password": "generated-password-123",
            },
        )
        mock_cloud_client.post.return_value = mock_response

        result = cloud_create_service(
            organization_id="org-123", name="test-service", provider="aws", region="us-east-1"
        )

        assert result["status"] == "success"
        assert result["data"]["service"]["name"] == "test-service"
        assert "password" in result["data"]

        # Verify the POST data
        call_args = mock_cloud_client.post.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services"
        post_data = call_args[1]["data"]
        assert post_data["name"] == "test-service"
        assert post_data["provider"] == "aws"
        assert post_data["region"] == "us-east-1"

    def test_cloud_update_service_state(self, mock_cloud_client):
        """Test updating service state."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_update_service_state

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-state",
            result={"id": "service-123", "state": "starting"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_service_state("org-123", "service-123", "start")

        assert result["status"] == "success"
        assert result["data"]["state"] == "starting"

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/state"
        assert call_args[1]["data"]["command"] == "start"

    def test_cloud_create_api_key(self, mock_cloud_client):
        """Test creating an API key."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_create_api_key

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-key",
            result={
                "key": {"id": "key-123", "name": "test-key", "roles": ["developer"]},
                "keyId": "generated-key-id",
                "keySecret": "generated-key-secret",
            },
        )
        mock_cloud_client.post.return_value = mock_response

        result = cloud_create_api_key(
            organization_id="org-123", name="test-key", roles=["developer"]
        )

        assert result["status"] == "success"
        assert "keyId" in result["data"]
        assert "keySecret" in result["data"]

        call_args = mock_cloud_client.post.call_args
        post_data = call_args[1]["data"]
        assert post_data["name"] == "test-key"
        assert post_data["roles"] == ["developer"]

    def test_cloud_get_available_regions(self):
        """Test getting available regions (static data)."""
        from mcp_clickhouse_cloud.cloud_tools import cloud_get_available_regions

        result = cloud_get_available_regions()

        assert result["status"] == "success"
        assert "data" in result
        assert "providers" in result["data"]
        assert "regions" in result["data"]

        # Check that we have the expected providers
        providers = result["data"]["providers"]
        assert "aws" in providers
        assert "gcp" in providers
        assert "azure" in providers

        # Check AWS regions
        aws_regions = result["data"]["regions"]["aws"]
        assert "us-east-1" in aws_regions
        assert "eu-west-1" in aws_regions
