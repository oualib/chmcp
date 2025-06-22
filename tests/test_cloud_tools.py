"""Tests for ClickHouse Cloud API tools."""

import pytest
from unittest.mock import Mock, patch
from chmcp.cloud_client import CloudAPIResponse, CloudAPIError


class TestCloudTools:
    """Test suite for ClickHouse Cloud API tools."""

    def test_cloud_list_organizations_success(self, mock_cloud_client):
        """Test successful organization listing."""
        from chmcp.cloud_tools import cloud_list_organizations

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
        from chmcp.cloud_tools import cloud_list_organizations

        # Mock error response
        mock_error = CloudAPIError(status=401, error="Unauthorized", request_id="test-request-456")
        mock_cloud_client.get.return_value = mock_error

        result = cloud_list_organizations()

        assert result["status"] == "error"
        assert result["error"] == "Unauthorized"
        assert result["status_code"] == 401

    def test_cloud_get_organization(self, mock_cloud_client):
        """Test getting specific organization details."""
        from chmcp.cloud_tools import cloud_get_organization

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

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_organization(self, mock_cloud_client):
        """Test updating organization details."""
        from chmcp.cloud_tools import cloud_update_organization

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-org",
            result={"id": "org-123", "name": "Updated Org Name"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_organization("org-123", name="Updated Org Name")

        assert result["status"] == "success"
        assert result["data"]["name"] == "Updated Org Name"

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123"
        assert call_args[1]["data"]["name"] == "Updated Org Name"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_organization_private_endpoint_info(self, mock_cloud_client):
        """Test getting organization private endpoint info."""
        from chmcp.cloud_tools import cloud_get_organization_private_endpoint_info

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-endpoint-info",
            result={"endpointServiceId": "vpce-service-123"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_organization_private_endpoint_info("org-123", "aws", "us-east-1")

        assert result["status"] == "success"
        assert result["data"]["endpointServiceId"] == "vpce-service-123"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/privateEndpointInfo/aws/us-east-1"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_organization_metrics(self, mock_cloud_client):
        """Test getting organization metrics."""
        from chmcp.cloud_tools import cloud_get_organization_metrics

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-org-metrics",
            result="# HELP metric_name Description\nmetric_name 42",
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_organization_metrics("org-123", filtered_metrics=True)

        assert result["status"] == "success"
        call_args = mock_cloud_client.get.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/prometheus"
        assert call_args[1]["params"]["filtered_metrics"] == "true"

    def test_cloud_list_services(self, mock_cloud_client):
        """Test listing services in an organization."""
        from chmcp.cloud_tools import cloud_list_services

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

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_service(self, mock_cloud_client):
        """Test getting service details."""
        from chmcp.cloud_tools import cloud_get_service

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-service",
            result={"id": "service-123", "name": "test-service", "state": "running"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_service("org-123", "service-123")

        assert result["status"] == "success"
        assert result["data"]["state"] == "running"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123"
        )

    def test_cloud_create_service(self, mock_cloud_client):
        """Test creating a new service."""
        from chmcp.cloud_tools import cloud_create_service

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

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_service(self, mock_cloud_client):
        """Test updating service details."""
        from chmcp.cloud_tools import cloud_update_service

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-service",
            result={"id": "service-123", "name": "updated-service"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_service("org-123", "service-123", name="updated-service")

        assert result["status"] == "success"
        assert result["data"]["name"] == "updated-service"

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123"
        assert call_args[1]["data"]["name"] == "updated-service"

    def test_cloud_update_service_state(self, mock_cloud_client):
        """Test updating service state."""
        from chmcp.cloud_tools import cloud_update_service_state

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

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_service_scaling(self, mock_cloud_client):
        """Test updating service scaling (deprecated method)."""
        from chmcp.cloud_tools import cloud_update_service_scaling

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-scaling",
            result={"id": "service-123", "minTotalMemoryGb": 48, "maxTotalMemoryGb": 360},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_service_scaling(
            "org-123", "service-123", min_total_memory_gb=48, max_total_memory_gb=360
        )

        assert result["status"] == "success"
        assert result["data"]["minTotalMemoryGb"] == 48

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/scaling"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_service_replica_scaling(self, mock_cloud_client):
        """Test updating service replica scaling (preferred method)."""
        from chmcp.cloud_tools import cloud_update_service_replica_scaling

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-replica-scaling",
            result={"id": "service-123", "minReplicaMemoryGb": 16, "maxReplicaMemoryGb": 120},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_service_replica_scaling(
            "org-123", "service-123", min_replica_memory_gb=16, max_replica_memory_gb=120
        )

        assert result["status"] == "success"
        assert result["data"]["minReplicaMemoryGb"] == 16

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/replicaScaling"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_service_password(self, mock_cloud_client):
        """Test updating service password."""
        from chmcp.cloud_tools import cloud_update_service_password

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-password-update",
            result={"password": "new-generated-password"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_service_password("org-123", "service-123")

        assert result["status"] == "success"
        assert "password" in result["data"]

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/password"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_create_service_private_endpoint(self, mock_cloud_client):
        """Test creating service private endpoint."""
        from chmcp.cloud_tools import cloud_create_service_private_endpoint

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-endpoint",
            result={"id": "endpoint-123", "description": "test endpoint"},
        )
        mock_cloud_client.post.return_value = mock_response

        result = cloud_create_service_private_endpoint(
            "org-123", "service-123", "endpoint-123", "test endpoint"
        )

        assert result["status"] == "success"
        assert result["data"]["id"] == "endpoint-123"

        call_args = mock_cloud_client.post.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/privateEndpoint"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_service_metrics(self, mock_cloud_client):
        """Test getting service metrics."""
        from chmcp.cloud_tools import cloud_get_service_metrics

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-service-metrics",
            result="# HELP metric_name Description\nmetric_name 42",
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_service_metrics("org-123", "service-123")

        assert result["status"] == "success"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/prometheus", params={}
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_delete_service(self, mock_cloud_client):
        """Test deleting service."""
        from chmcp.cloud_tools import cloud_delete_service

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-delete-service",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_delete_service("org-123", "service-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123"
        )

    # Query Endpoints Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_query_endpoint_config(self, mock_cloud_client):
        """Test getting query endpoint configuration."""
        from chmcp.cloud_tools import cloud_get_query_endpoint_config

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-query-config",
            result={"id": "config-123", "roles": ["sql_console_read_only"]},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_query_endpoint_config("org-123", "service-123")

        assert result["status"] == "success"
        assert "roles" in result["data"]
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/queryEndpoint"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_create_query_endpoint_config(self, mock_cloud_client):
        """Test creating query endpoint configuration."""
        from chmcp.cloud_tools import cloud_create_query_endpoint_config

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-query-config",
            result={"id": "config-123", "roles": ["sql_console_admin"]},
        )
        mock_cloud_client.post.return_value = mock_response

        result = cloud_create_query_endpoint_config(
            "org-123", "service-123", ["sql_console_admin"], ["key1"], "example.com"
        )

        assert result["status"] == "success"
        call_args = mock_cloud_client.post.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/queryEndpoint"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_delete_query_endpoint_config(self, mock_cloud_client):
        """Test deleting query endpoint configuration."""
        from chmcp.cloud_tools import cloud_delete_query_endpoint_config

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-delete-query-config",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_delete_query_endpoint_config("org-123", "service-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/queryEndpoint"
        )

    # API Key Management Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_api_keys(self, mock_cloud_client):
        """Test listing API keys."""
        from chmcp.cloud_tools import cloud_list_api_keys

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-keys",
            result=[{"id": "key-123", "name": "test-key", "state": "enabled"}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_api_keys("org-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123/keys")

    def test_cloud_create_api_key(self, mock_cloud_client):
        """Test creating an API key."""
        from chmcp.cloud_tools import cloud_create_api_key

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

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_api_key(self, mock_cloud_client):
        """Test getting specific API key details."""
        from chmcp.cloud_tools import cloud_get_api_key

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-key",
            result={"id": "key-123", "name": "test-key", "state": "enabled"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_api_key("org-123", "key-123")

        assert result["status"] == "success"
        assert result["data"]["state"] == "enabled"
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123/keys/key-123")

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_api_key(self, mock_cloud_client):
        """Test updating API key properties."""
        from chmcp.cloud_tools import cloud_update_api_key

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-key",
            result={"id": "key-123", "name": "updated-key", "state": "disabled"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_api_key("org-123", "key-123", name="updated-key", state="disabled")

        assert result["status"] == "success"
        assert result["data"]["name"] == "updated-key"

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/keys/key-123"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_delete_api_key(self, mock_cloud_client):
        """Test deleting API key."""
        from chmcp.cloud_tools import cloud_delete_api_key

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-delete-key",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_delete_api_key("org-123", "key-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with("/v1/organizations/org-123/keys/key-123")

    # Member Management Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_members(self, mock_cloud_client):
        """Test listing organization members."""
        from chmcp.cloud_tools import cloud_list_members

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-members",
            result=[{"userId": "user-123", "name": "John Doe", "role": "admin"}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_members("org-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["role"] == "admin"
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123/members")

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_member(self, mock_cloud_client):
        """Test getting specific member details."""
        from chmcp.cloud_tools import cloud_get_member

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-member",
            result={"userId": "user-123", "name": "John Doe", "role": "developer"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_member("org-123", "user-123")

        assert result["status"] == "success"
        assert result["data"]["role"] == "developer"
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123/members/user-123")

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_member_role(self, mock_cloud_client):
        """Test updating member role."""
        from chmcp.cloud_tools import cloud_update_member_role

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-member",
            result={"userId": "user-123", "role": "developer"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_member_role("org-123", "user-123", "developer")

        assert result["status"] == "success"
        assert result["data"]["role"] == "developer"

        call_args = mock_cloud_client.patch.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/members/user-123"
        assert call_args[1]["data"]["role"] == "developer"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_remove_member(self, mock_cloud_client):
        """Test removing organization member."""
        from chmcp.cloud_tools import cloud_remove_member

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-remove-member",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_remove_member("org-123", "user-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with(
            "/v1/organizations/org-123/members/user-123"
        )

    # Invitation Management Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_invitations(self, mock_cloud_client):
        """Test listing organization invitations."""
        from chmcp.cloud_tools import cloud_list_invitations

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-invitations",
            result=[{"id": "invite-123", "role": "developer", "createdAt": "2024-01-01T00:00:00Z"}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_invitations("org-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        mock_cloud_client.get.assert_called_once_with("/v1/organizations/org-123/invitations")

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_create_invitation(self, mock_cloud_client):
        """Test creating organization invitation."""
        from chmcp.cloud_tools import cloud_create_invitation

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-invitation",
            result={"id": "invite-123", "role": "developer"},
        )
        mock_cloud_client.post.return_value = mock_response

        result = cloud_create_invitation("org-123", "test@example.com", "developer")

        assert result["status"] == "success"
        assert result["data"]["role"] == "developer"

        call_args = mock_cloud_client.post.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/invitations"
        assert call_args[1]["data"]["email"] == "test@example.com"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_invitation(self, mock_cloud_client):
        """Test getting specific invitation details."""
        from chmcp.cloud_tools import cloud_get_invitation

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-invitation",
            result={"id": "invite-123", "role": "developer", "email": "test@example.com"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_invitation("org-123", "invite-123")

        assert result["status"] == "success"
        assert result["data"]["role"] == "developer"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/invitations/invite-123"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_delete_invitation(self, mock_cloud_client):
        """Test deleting organization invitation."""
        from chmcp.cloud_tools import cloud_delete_invitation

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-delete-invitation",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_delete_invitation("org-123", "invite-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with(
            "/v1/organizations/org-123/invitations/invite-123"
        )

    # Backup Management Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_backups(self, mock_cloud_client):
        """Test listing service backups."""
        from chmcp.cloud_tools import cloud_list_backups

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-backups",
            result=[{"id": "backup-123", "status": "done", "sizeInBytes": 1024}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_backups("org-123", "service-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["status"] == "done"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/backups"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_backup(self, mock_cloud_client):
        """Test getting backup details."""
        from chmcp.cloud_tools import cloud_get_backup

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-backup",
            result={"id": "backup-123", "status": "done", "durationInSeconds": 300},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_backup("org-123", "service-123", "backup-123")

        assert result["status"] == "success"
        assert result["data"]["durationInSeconds"] == 300
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/backups/backup-123"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_backup_configuration(self, mock_cloud_client):
        """Test getting backup configuration."""
        from chmcp.cloud_tools import cloud_get_backup_configuration

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-backup-config",
            result={"backupPeriodInHours": 24, "backupRetentionPeriodInHours": 168},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_backup_configuration("org-123", "service-123")

        assert result["status"] == "success"
        assert result["data"]["backupPeriodInHours"] == 24
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/backupConfiguration"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_backup_configuration(self, mock_cloud_client):
        """Test updating backup configuration."""
        from chmcp.cloud_tools import cloud_update_backup_configuration

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-backup-config",
            result={"backupPeriodInHours": 12, "backupRetentionPeriodInHours": 72},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_backup_configuration(
            "org-123", "service-123", backup_period_in_hours=12, backup_retention_period_in_hours=72
        )

        assert result["status"] == "success"
        assert result["data"]["backupPeriodInHours"] == 12

        call_args = mock_cloud_client.patch.call_args
        assert (
            call_args[0][0] == "/v1/organizations/org-123/services/service-123/backupConfiguration"
        )

    # Activity & Audit Log Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_activities(self, mock_cloud_client):
        """Test listing organization activities."""
        from chmcp.cloud_tools import cloud_list_activities

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-activities",
            result=[
                {
                    "id": "activity-123",
                    "type": "create_service",
                    "createdAt": "2024-01-01T00:00:00Z",
                }
            ],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_activities("org-123", from_date="2024-01-01", to_date="2024-01-31")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["type"] == "create_service"

        call_args = mock_cloud_client.get.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/activities"
        assert call_args[1]["params"]["from_date"] == "2024-01-01"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_activity(self, mock_cloud_client):
        """Test getting activity details."""
        from chmcp.cloud_tools import cloud_get_activity

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-activity",
            result={"id": "activity-123", "type": "create_service", "actorType": "user"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_activity("org-123", "activity-123")

        assert result["status"] == "success"
        assert result["data"]["actorType"] == "user"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/activities/activity-123"
        )

    # Usage & Cost Analytics Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_usage_cost(self, mock_cloud_client):
        """Test getting usage cost data."""
        from chmcp.cloud_tools import cloud_get_usage_cost

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-usage-cost",
            result={"grandTotalCHC": 150.50, "costs": []},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_usage_cost("org-123", "2024-01-01", "2024-01-31")

        assert result["status"] == "success"
        assert result["data"]["grandTotalCHC"] == 150.50

        call_args = mock_cloud_client.get.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/usageCost"
        assert call_args[1]["params"]["from_date"] == "2024-01-01"
        assert call_args[1]["params"]["to_date"] == "2024-01-31"

    # Private Endpoint Tests
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_private_endpoint_config(self, mock_cloud_client):
        """Test getting private endpoint configuration."""
        from chmcp.cloud_tools import cloud_get_private_endpoint_config

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-private-endpoint-config",
            result={"endpointServiceId": "vpce-service-123", "privateDnsHostname": "test.dns"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_private_endpoint_config("org-123", "service-123")

        assert result["status"] == "success"
        assert result["data"]["endpointServiceId"] == "vpce-service-123"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/privateEndpointConfig"
        )

    # Reverse Private Endpoints Tests (Beta)
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_reverse_private_endpoints(self, mock_cloud_client):
        """Test listing reverse private endpoints."""
        from chmcp.cloud_tools import cloud_list_reverse_private_endpoints

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-reverse-endpoints",
            result=[{"id": "rpe-123", "description": "test endpoint", "status": "Ready"}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_reverse_private_endpoints("org-123", "service-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/reversePrivateEndpoints"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_create_reverse_private_endpoint(self, mock_cloud_client):
        """Test creating reverse private endpoint."""
        from chmcp.cloud_tools import cloud_create_reverse_private_endpoint

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-reverse-endpoint",
            result={
                "id": "rpe-123",
                "description": "test endpoint",
                "type": "VPC_ENDPOINT_SERVICE",
            },
        )
        mock_cloud_client.post.return_value = mock_response

        result = cloud_create_reverse_private_endpoint(
            "org-123", "service-123", "test endpoint", "VPC_ENDPOINT_SERVICE"
        )

        assert result["status"] == "success"
        assert result["data"]["type"] == "VPC_ENDPOINT_SERVICE"

        call_args = mock_cloud_client.post.call_args
        assert (
            call_args[0][0]
            == "/v1/organizations/org-123/services/service-123/reversePrivateEndpoints"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_reverse_private_endpoint(self, mock_cloud_client):
        """Test getting reverse private endpoint details."""
        from chmcp.cloud_tools import cloud_get_reverse_private_endpoint

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-reverse-endpoint",
            result={"id": "rpe-123", "status": "Ready"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_reverse_private_endpoint("org-123", "service-123", "rpe-123")

        assert result["status"] == "success"
        assert result["data"]["status"] == "Ready"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/reversePrivateEndpoints/rpe-123"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_delete_reverse_private_endpoint(self, mock_cloud_client):
        """Test deleting reverse private endpoint."""
        from chmcp.cloud_tools import cloud_delete_reverse_private_endpoint

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-delete-reverse-endpoint",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_delete_reverse_private_endpoint("org-123", "service-123", "rpe-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/reversePrivateEndpoints/rpe-123"
        )

    # ClickPipes Tests (Beta)
    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_list_clickpipes(self, mock_cloud_client):
        """Test listing ClickPipes."""
        from chmcp.cloud_tools import cloud_list_clickpipes

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-list-clickpipes",
            result=[{"id": "pipe-123", "name": "test-pipe", "state": "running"}],
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_list_clickpipes("org-123", "service-123")

        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["state"] == "running"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/clickpipes"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_create_clickpipe(self, mock_cloud_client):
        """Test creating a ClickPipe."""
        from chmcp.cloud_tools import cloud_create_clickpipe

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-create-clickpipe",
            result={"id": "pipe-123", "name": "test-pipe", "state": "creating"},
        )
        mock_cloud_client.post.return_value = mock_response

        source_config = {"kafka": {"brokers": "broker1:9092", "topics": "test-topic"}}
        destination_config = {"database": "default", "table": "test_table"}

        result = cloud_create_clickpipe(
            "org-123",
            "service-123",
            "test-pipe",
            "Test ClickPipe",
            source_config,
            destination_config,
        )

        assert result["status"] == "success"
        assert result["data"]["name"] == "test-pipe"

        call_args = mock_cloud_client.post.call_args
        assert call_args[0][0] == "/v1/organizations/org-123/services/service-123/clickpipes"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_get_clickpipe(self, mock_cloud_client):
        """Test getting ClickPipe details."""
        from chmcp.cloud_tools import cloud_get_clickpipe

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-get-clickpipe",
            result={"id": "pipe-123", "name": "test-pipe", "state": "running"},
        )
        mock_cloud_client.get.return_value = mock_response

        result = cloud_get_clickpipe("org-123", "service-123", "pipe-123")

        assert result["status"] == "success"
        assert result["data"]["state"] == "running"
        mock_cloud_client.get.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/clickpipes/pipe-123"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_clickpipe(self, mock_cloud_client):
        """Test updating a ClickPipe."""
        from chmcp.cloud_tools import cloud_update_clickpipe

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-update-clickpipe",
            result={"id": "pipe-123", "name": "updated-pipe"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_clickpipe("org-123", "service-123", "pipe-123", name="updated-pipe")

        assert result["status"] == "success"
        assert result["data"]["name"] == "updated-pipe"

        call_args = mock_cloud_client.patch.call_args
        assert (
            call_args[0][0] == "/v1/organizations/org-123/services/service-123/clickpipes/pipe-123"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_clickpipe_scaling(self, mock_cloud_client):
        """Test updating ClickPipe scaling."""
        from chmcp.cloud_tools import cloud_update_clickpipe_scaling

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-clickpipe-scaling",
            result={"id": "pipe-123", "scaling": {"replicas": 3}},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_clickpipe_scaling("org-123", "service-123", "pipe-123", replicas=3)

        assert result["status"] == "success"
        call_args = mock_cloud_client.patch.call_args
        assert (
            call_args[0][0]
            == "/v1/organizations/org-123/services/service-123/clickpipes/pipe-123/scaling"
        )

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_update_clickpipe_state(self, mock_cloud_client):
        """Test updating ClickPipe state."""
        from chmcp.cloud_tools import cloud_update_clickpipe_state

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-clickpipe-state",
            result={"id": "pipe-123", "state": "starting"},
        )
        mock_cloud_client.patch.return_value = mock_response

        result = cloud_update_clickpipe_state("org-123", "service-123", "pipe-123", "start")

        assert result["status"] == "success"
        assert result["data"]["state"] == "starting"

        call_args = mock_cloud_client.patch.call_args
        assert (
            call_args[0][0]
            == "/v1/organizations/org-123/services/service-123/clickpipes/pipe-123/state"
        )
        assert call_args[1]["data"]["command"] == "start"

    @pytest.mark.skip(reason="Requires live ClickHouse Cloud API credentials")
    def test_cloud_delete_clickpipe(self, mock_cloud_client):
        """Test deleting ClickPipe."""
        from chmcp.cloud_tools import cloud_delete_clickpipe

        mock_response = CloudAPIResponse(
            status=200,
            request_id="test-delete-clickpipe",
            result=None,
        )
        mock_cloud_client.delete.return_value = mock_response

        result = cloud_delete_clickpipe("org-123", "service-123", "pipe-123")

        assert result["status"] == "success"
        mock_cloud_client.delete.assert_called_once_with(
            "/v1/organizations/org-123/services/service-123/clickpipes/pipe-123"
        )

    # Utility Tests
    def test_cloud_get_available_regions(self):
        """Test getting available regions (static data)."""
        from chmcp.cloud_tools import cloud_get_available_regions

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

    # Error handling tests
    def test_handle_api_response_error(self):
        """Test error response handling."""
        from chmcp.cloud_tools import _handle_api_response

        error = CloudAPIError(status=404, error="Not Found", request_id="error-request")
        result = _handle_api_response(error)

        assert result["status"] == "error"
        assert result["error"] == "Not Found"
        assert result["status_code"] == 404
        assert result["request_id"] == "error-request"

    def test_handle_api_response_success(self):
        """Test success response handling."""
        from chmcp.cloud_tools import _handle_api_response

        response = CloudAPIResponse(
            status=200, request_id="success-request", result={"data": "test"}
        )
        result = _handle_api_response(response)

        assert result["status"] == "success"
        assert result["data"] == {"data": "test"}
        assert result["status_code"] == 200
        assert result["request_id"] == "success-request"
