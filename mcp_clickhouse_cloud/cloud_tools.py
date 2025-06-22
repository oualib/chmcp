# Copyright 2025 Badr Ouali
# SPDX-License-Identifier: Apache-2.0

"""ClickHouse Cloud MCP Tools.

This module provides comprehensive MCP tools for all ClickHouse Cloud API operations
including organizations, services, API keys, members, backups, ClickPipes, and more.
"""

import logging
from typing import Any, Dict, List, Optional

from .cloud_client import CloudAPIError, CloudAPIResponse, create_cloud_client
from .mcp_server import mcp

logger = logging.getLogger(__name__)


def _handle_api_response(response) -> Dict[str, Any]:
    """Handle API response and return formatted result.

    Args:
        response: CloudAPIResponse or CloudAPIError

    Returns:
        Formatted response dictionary
    """
    if isinstance(response, CloudAPIError):
        return {
            "status": "error",
            "error": response.error,
            "status_code": response.status,
            "request_id": response.request_id,
        }

    return {
        "status": "success",
        "data": response.result,
        "status_code": response.status,
        "request_id": response.request_id,
    }


# Organization Tools
@mcp.tool()
def cloud_list_organizations() -> Dict[str, Any]:
    """List available ClickHouse Cloud organizations.

    Returns list of organizations associated with the API key.
    """
    logger.info("Listing ClickHouse Cloud organizations")
    client = create_cloud_client()
    response = client.get("/v1/organizations")
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_organization(organization_id: str) -> Dict[str, Any]:
    """Get details of a specific organization.

    Args:
        organization_id: UUID of the organization

    Returns:
        Organization details
    """
    logger.info(f"Getting organization details for {organization_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}")
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_organization(
    organization_id: str, name: Optional[str] = None, private_endpoints: Optional[Dict] = None
) -> Dict[str, Any]:
    """Update organization details.

    Args:
        organization_id: UUID of the organization
        name: New organization name
        private_endpoints: Private endpoints configuration with add/remove operations

    Returns:
        Updated organization details
    """
    logger.info(f"Updating organization {organization_id}")
    client = create_cloud_client()

    data = {}
    if name is not None:
        data["name"] = name
    if private_endpoints is not None:
        data["privateEndpoints"] = private_endpoints

    response = client.patch(f"/v1/organizations/{organization_id}", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_organization_metrics(
    organization_id: str, filtered_metrics: Optional[bool] = None
) -> Dict[str, Any]:
    """Get Prometheus metrics for all services in an organization.

    Args:
        organization_id: UUID of the organization
        filtered_metrics: Return filtered list of metrics

    Returns:
        Prometheus metrics data
    """
    logger.info(f"Getting metrics for organization {organization_id}")
    client = create_cloud_client()

    params = {}
    if filtered_metrics is not None:
        params["filtered_metrics"] = str(filtered_metrics).lower()

    response = client.get(f"/v1/organizations/{organization_id}/prometheus", params=params)
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_organization_private_endpoint_info(
    organization_id: str, cloud_provider: str, region: str
) -> Dict[str, Any]:
    """Get private endpoint information for organization.

    Args:
        organization_id: UUID of the organization
        cloud_provider: Cloud provider identifier (aws, gcp, azure)
        region: Region identifier

    Returns:
        Private endpoint information
    """
    logger.info(f"Getting private endpoint info for organization {organization_id}")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/privateEndpointInfo/{cloud_provider}/{region}"
    )
    return _handle_api_response(response)


# Service Tools
@mcp.tool()
def cloud_list_services(organization_id: str) -> Dict[str, Any]:
    """List all services in an organization.

    Args:
        organization_id: UUID of the organization

    Returns:
        List of services
    """
    logger.info(f"Listing services for organization {organization_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/services")
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_service(organization_id: str, service_id: str) -> Dict[str, Any]:
    """Get details of a specific service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        Service details
    """
    logger.info(f"Getting service {service_id} details")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}")
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_service(
    organization_id: str,
    name: str,
    provider: str,
    region: str,
    tier: Optional[str] = "production",
    min_replica_memory_gb: Optional[int] = 16,
    max_replica_memory_gb: Optional[int] = 120,
    num_replicas: Optional[int] = 3,
    idle_scaling: Optional[bool] = True,
    idle_timeout_minutes: Optional[int] = None,
    ip_access_list: Optional[List[Dict[str, str]]] = None,
    is_readonly: Optional[bool] = None,
    data_warehouse_id: Optional[str] = None,
    backup_id: Optional[str] = None,
    encryption_key: Optional[str] = None,
    encryption_assumed_role_identifier: Optional[str] = None,
    private_endpoint_ids: Optional[List[str]] = None,
    private_preview_terms_checked: Optional[bool] = None,
    release_channel: Optional[str] = None,
    byoc_id: Optional[str] = None,
    has_transparent_data_encryption: Optional[bool] = None,
    endpoints: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Create a new ClickHouse Cloud service.

    Args:
        organization_id: UUID of the organization
        name: Service name (alphanumeric with spaces, up to 50 chars)
        provider: Cloud provider (aws, gcp, azure)
        region: Service region (e.g., us-east-1, eu-west-1, etc.)
        tier: Service tier (development, production)
        min_replica_memory_gb: Minimum memory per replica in GB (multiple of 4, min 8)
        max_replica_memory_gb: Maximum memory per replica in GB (multiple of 4, max 356)
        num_replicas: Number of replicas (1-20)
        idle_scaling: Enable idle scaling to zero
        idle_timeout_minutes: Idle timeout in minutes (min 5)
        ip_access_list: List of IP access entries [{"source": "IP/CIDR", "description": "desc"}]
        is_readonly: True if this service is read-only
        data_warehouse_id: Data warehouse containing this service
        backup_id: Optional backup ID used as initial state
        encryption_key: Optional customer provided disk encryption key
        encryption_assumed_role_identifier: Optional role to use for disk encryption
        private_endpoint_ids: List of private endpoint IDs to associate
        private_preview_terms_checked: Accept private preview terms
        release_channel: Release channel (default, fast)
        byoc_id: Bring Your Own Cloud ID
        has_transparent_data_encryption: Enable Transparent Data Encryption
        endpoints: List of service endpoints to enable or disable

    Returns:
        Created service details and password
    """
    logger.info(f"Creating service {name} in organization {organization_id}")
    client = create_cloud_client()

    data = {
        "name": name,
        "provider": provider,
        "region": region,
        "tier": tier,
        "minReplicaMemoryGb": min_replica_memory_gb,
        "maxReplicaMemoryGb": max_replica_memory_gb,
        "numReplicas": num_replicas,
        "idleScaling": idle_scaling,
    }

    # Add optional parameters
    if idle_timeout_minutes is not None:
        data["idleTimeoutMinutes"] = idle_timeout_minutes
    if ip_access_list is not None:
        data["ipAccessList"] = ip_access_list
    if is_readonly is not None:
        data["isReadonly"] = is_readonly
    if data_warehouse_id is not None:
        data["dataWarehouseId"] = data_warehouse_id
    if backup_id is not None:
        data["backupId"] = backup_id
    if encryption_key is not None:
        data["encryptionKey"] = encryption_key
    if encryption_assumed_role_identifier is not None:
        data["encryptionAssumedRoleIdentifier"] = encryption_assumed_role_identifier
    if private_endpoint_ids is not None:
        data["privateEndpointIds"] = private_endpoint_ids
    if private_preview_terms_checked is not None:
        data["privatePreviewTermsChecked"] = private_preview_terms_checked
    if release_channel is not None:
        data["releaseChannel"] = release_channel
    if byoc_id is not None:
        data["byocId"] = byoc_id
    if has_transparent_data_encryption is not None:
        data["hasTransparentDataEncryption"] = has_transparent_data_encryption
    if endpoints is not None:
        data["endpoints"] = endpoints

    response = client.post(f"/v1/organizations/{organization_id}/services", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_service(
    organization_id: str,
    service_id: str,
    name: Optional[str] = None,
    ip_access_list: Optional[Dict] = None,
    private_endpoint_ids: Optional[Dict] = None,
    release_channel: Optional[str] = None,
    endpoints: Optional[List[Dict]] = None,
    transparent_data_encryption_key_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Update basic service details like service name or IP access list.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        name: Service name
        ip_access_list: IP access list with add/remove operations
        private_endpoint_ids: Private endpoint IDs with add/remove operations
        release_channel: Release channel (default, fast)
        endpoints: List of service endpoints to change
        transparent_data_encryption_key_id: The id of the key to rotate

    Returns:
        Updated service details
    """
    logger.info(f"Updating service {service_id}")
    client = create_cloud_client()

    data = {}
    if name is not None:
        data["name"] = name
    if ip_access_list is not None:
        data["ipAccessList"] = ip_access_list
    if private_endpoint_ids is not None:
        data["privateEndpointIds"] = private_endpoint_ids
    if release_channel is not None:
        data["releaseChannel"] = release_channel
    if endpoints is not None:
        data["endpoints"] = endpoints
    if transparent_data_encryption_key_id is not None:
        data["transparentDataEncryptionKeyId"] = transparent_data_encryption_key_id

    response = client.patch(f"/v1/organizations/{organization_id}/services/{service_id}", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_service_state(
    organization_id: str, service_id: str, command: str
) -> Dict[str, Any]:
    """Start or stop a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        command: Command to execute (start, stop)

    Returns:
        Updated service details
    """
    logger.info(f"Updating service {service_id} state: {command}")
    client = create_cloud_client()

    data = {"command": command}
    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/state", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_service_scaling(
    organization_id: str,
    service_id: str,
    min_total_memory_gb: Optional[int] = None,
    max_total_memory_gb: Optional[int] = None,
    num_replicas: Optional[int] = None,
    idle_scaling: Optional[bool] = None,
    idle_timeout_minutes: Optional[int] = None,
) -> Dict[str, Any]:
    """Update service scaling parameters (deprecated method).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        min_total_memory_gb: Minimum total memory in GB (deprecated)
        max_total_memory_gb: Maximum total memory in GB (deprecated)
        num_replicas: Number of replicas
        idle_scaling: Enable idle scaling
        idle_timeout_minutes: Idle timeout in minutes

    Returns:
        Updated service details
    """
    logger.info(f"Updating service {service_id} scaling (deprecated method)")
    client = create_cloud_client()

    data = {}
    if min_total_memory_gb is not None:
        data["minTotalMemoryGb"] = min_total_memory_gb
    if max_total_memory_gb is not None:
        data["maxTotalMemoryGb"] = max_total_memory_gb
    if num_replicas is not None:
        data["numReplicas"] = num_replicas
    if idle_scaling is not None:
        data["idleScaling"] = idle_scaling
    if idle_timeout_minutes is not None:
        data["idleTimeoutMinutes"] = idle_timeout_minutes

    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/scaling", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_service_replica_scaling(
    organization_id: str,
    service_id: str,
    min_replica_memory_gb: Optional[int] = None,
    max_replica_memory_gb: Optional[int] = None,
    num_replicas: Optional[int] = None,
    idle_scaling: Optional[bool] = None,
    idle_timeout_minutes: Optional[int] = None,
) -> Dict[str, Any]:
    """Update service replica scaling parameters (preferred method).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        min_replica_memory_gb: Minimum memory per replica in GB
        max_replica_memory_gb: Maximum memory per replica in GB
        num_replicas: Number of replicas
        idle_scaling: Enable idle scaling
        idle_timeout_minutes: Idle timeout in minutes

    Returns:
        Updated service details
    """
    logger.info(f"Updating service {service_id} replica scaling")
    client = create_cloud_client()

    data = {}
    if min_replica_memory_gb is not None:
        data["minReplicaMemoryGb"] = min_replica_memory_gb
    if max_replica_memory_gb is not None:
        data["maxReplicaMemoryGb"] = max_replica_memory_gb
    if num_replicas is not None:
        data["numReplicas"] = num_replicas
    if idle_scaling is not None:
        data["idleScaling"] = idle_scaling
    if idle_timeout_minutes is not None:
        data["idleTimeoutMinutes"] = idle_timeout_minutes

    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/replicaScaling", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_service_password(
    organization_id: str,
    service_id: str,
    new_password_hash: Optional[str] = None,
    new_double_sha1_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """Set a new password for the service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        new_password_hash: Optional password hash to avoid password transmission
        new_double_sha1_hash: Optional double SHA1 password hash for MySQL protocol

    Returns:
        New password details
    """
    logger.info(f"Updating password for service {service_id}")
    client = create_cloud_client()

    data = {}
    if new_password_hash is not None:
        data["newPasswordHash"] = new_password_hash
    if new_double_sha1_hash is not None:
        data["newDoubleSha1Hash"] = new_double_sha1_hash

    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/password", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_service_private_endpoint(
    organization_id: str, service_id: str, id: str, description: str
) -> Dict[str, Any]:
    """Create a new private endpoint for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        id: Private endpoint identifier
        description: Description of private endpoint

    Returns:
        Created private endpoint details
    """
    logger.info(f"Creating private endpoint for service {service_id}")
    client = create_cloud_client()

    data = {"id": id, "description": description}

    response = client.post(
        f"/v1/organizations/{organization_id}/services/{service_id}/privateEndpoint", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_service_metrics(
    organization_id: str, service_id: str, filtered_metrics: Optional[bool] = None
) -> Dict[str, Any]:
    """Get Prometheus metrics for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        filtered_metrics: Return filtered list of metrics

    Returns:
        Service metrics data
    """
    logger.info(f"Getting metrics for service {service_id}")
    client = create_cloud_client()

    params = {}
    if filtered_metrics is not None:
        params["filtered_metrics"] = str(filtered_metrics).lower()

    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/prometheus", params=params
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_service(organization_id: str, service_id: str) -> Dict[str, Any]:
    """Delete a service (must be stopped first).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        Deletion confirmation
    """
    logger.info(f"Deleting service {service_id}")
    client = create_cloud_client()
    response = client.delete(f"/v1/organizations/{organization_id}/services/{service_id}")
    return _handle_api_response(response)


# Query Endpoints (Experimental)
@mcp.tool()
def cloud_get_query_endpoint_config(organization_id: str, service_id: str) -> Dict[str, Any]:
    """Get query endpoint configuration for a service (experimental).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        Query endpoint configuration
    """
    logger.info(f"Getting query endpoint config for service {service_id}")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/queryEndpoint"
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_query_endpoint_config(
    organization_id: str,
    service_id: str,
    roles: List[str],
    open_api_keys: List[str],
    allowed_origins: str,
) -> Dict[str, Any]:
    """Create query endpoint configuration for a service (experimental).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        roles: List of roles (sql_console_read_only, sql_console_admin)
        open_api_keys: List of open API keys
        allowed_origins: Allowed origins as comma separated list of domains

    Returns:
        Created query endpoint configuration
    """
    logger.info(f"Creating query endpoint config for service {service_id}")
    client = create_cloud_client()

    data = {"roles": roles, "openApiKeys": open_api_keys, "allowedOrigins": allowed_origins}

    response = client.post(
        f"/v1/organizations/{organization_id}/services/{service_id}/queryEndpoint", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_query_endpoint_config(organization_id: str, service_id: str) -> Dict[str, Any]:
    """Delete query endpoint configuration for a service (experimental).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        Deletion confirmation
    """
    logger.info(f"Deleting query endpoint config for service {service_id}")
    client = create_cloud_client()
    response = client.delete(
        f"/v1/organizations/{organization_id}/services/{service_id}/queryEndpoint"
    )
    return _handle_api_response(response)


# API Key Tools
@mcp.tool()
def cloud_list_api_keys(organization_id: str) -> Dict[str, Any]:
    """List all API keys in an organization.

    Args:
        organization_id: UUID of the organization

    Returns:
        List of API keys (secrets are not included, only metadata)
    """
    logger.info(f"Listing API keys for organization {organization_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/keys")
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_api_key(
    organization_id: str,
    name: str,
    roles: List[str],
    expire_at: Optional[str] = None,
    state: Optional[str] = "enabled",
    hash_data: Optional[Dict] = None,
    ip_access_list: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    """Create a new API key.

    Args:
        organization_id: UUID of the organization
        name: Key name
        roles: List of roles (admin, developer, query_endpoints)
        expire_at: Expiration timestamp in ISO-8601 format (optional)
        state: Initial state (enabled, disabled)
        hash_data: Optional hash data for the key
        ip_access_list: List of IP access entries [{"source": "IP/CIDR", "description": "desc"}]

    Returns:
        Created API key details and credentials (keyId and keySecret)
    """
    logger.info(f"Creating API key {name} in organization {organization_id}")
    client = create_cloud_client()

    data = {"name": name, "roles": roles, "state": state}

    if expire_at is not None:
        data["expireAt"] = expire_at
    if hash_data is not None:
        data["hashData"] = hash_data
    if ip_access_list is not None:
        data["ipAccessList"] = ip_access_list

    response = client.post(f"/v1/organizations/{organization_id}/keys", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_api_key(organization_id: str, key_id: str) -> Dict[str, Any]:
    """Get details of a specific API key.

    Args:
        organization_id: UUID of the organization
        key_id: UUID of the API key

    Returns:
        API key details
    """
    logger.info(f"Getting API key {key_id} details")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/keys/{key_id}")
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_api_key(
    organization_id: str,
    key_id: str,
    name: Optional[str] = None,
    roles: Optional[List[str]] = None,
    expire_at: Optional[str] = None,
    state: Optional[str] = None,
    ip_access_list: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Update API key properties.

    Args:
        organization_id: UUID of the organization
        key_id: UUID of the API key
        name: Key name
        roles: List of roles (admin, developer, query_endpoints)
        expire_at: Expiration timestamp in ISO-8601 format
        state: State of the key (enabled, disabled)
        ip_access_list: List of IP access entries

    Returns:
        Updated API key details
    """
    logger.info(f"Updating API key {key_id}")
    client = create_cloud_client()

    data = {}
    if name is not None:
        data["name"] = name
    if roles is not None:
        data["roles"] = roles
    if expire_at is not None:
        data["expireAt"] = expire_at
    if state is not None:
        data["state"] = state
    if ip_access_list is not None:
        data["ipAccessList"] = ip_access_list

    response = client.patch(f"/v1/organizations/{organization_id}/keys/{key_id}", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_api_key(organization_id: str, key_id: str) -> Dict[str, Any]:
    """Delete an API key.

    Args:
        organization_id: UUID of the organization
        key_id: UUID of the API key

    Returns:
        Deletion confirmation
    """
    logger.info(f"Deleting API key {key_id}")
    client = create_cloud_client()
    response = client.delete(f"/v1/organizations/{organization_id}/keys/{key_id}")
    return _handle_api_response(response)


# Member Management Tools
@mcp.tool()
def cloud_list_members(organization_id: str) -> Dict[str, Any]:
    """List all members in an organization.

    Args:
        organization_id: UUID of the organization

    Returns:
        List of organization members with their roles and details
    """
    logger.info(f"Listing members for organization {organization_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/members")
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_member(organization_id: str, user_id: str) -> Dict[str, Any]:
    """Get details of a specific organization member.

    Args:
        organization_id: UUID of the organization
        user_id: UUID of the user

    Returns:
        Member details
    """
    logger.info(f"Getting member {user_id} details")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/members/{user_id}")
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_member_role(organization_id: str, user_id: str, role: str) -> Dict[str, Any]:
    """Update organization member role.

    Args:
        organization_id: UUID of the organization
        user_id: UUID of the user
        role: New role (admin, developer)

    Returns:
        Updated member details
    """
    logger.info(f"Updating member {user_id} role to {role}")
    client = create_cloud_client()

    data = {"role": role}
    response = client.patch(f"/v1/organizations/{organization_id}/members/{user_id}", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_remove_member(organization_id: str, user_id: str) -> Dict[str, Any]:
    """Remove a member from the organization.

    Args:
        organization_id: UUID of the organization
        user_id: UUID of the user to remove

    Returns:
        Removal confirmation
    """
    logger.info(f"Removing member {user_id} from organization {organization_id}")
    client = create_cloud_client()
    response = client.delete(f"/v1/organizations/{organization_id}/members/{user_id}")
    return _handle_api_response(response)


# Invitation Tools
@mcp.tool()
def cloud_list_invitations(organization_id: str) -> Dict[str, Any]:
    """List all pending invitations for an organization.

    Args:
        organization_id: UUID of the organization

    Returns:
        List of pending invitations
    """
    logger.info(f"Listing invitations for organization {organization_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/invitations")
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_invitation(organization_id: str, email: str, role: str) -> Dict[str, Any]:
    """Create an invitation to join the organization.

    Args:
        organization_id: UUID of the organization
        email: Email address of the person to invite
        role: Role to assign (admin, developer)

    Returns:
        Created invitation details
    """
    logger.info(f"Creating invitation for {email} in organization {organization_id}")
    client = create_cloud_client()

    data = {"email": email, "role": role}

    response = client.post(f"/v1/organizations/{organization_id}/invitations", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_invitation(organization_id: str, invitation_id: str) -> Dict[str, Any]:
    """Get details of a specific invitation.

    Args:
        organization_id: UUID of the organization
        invitation_id: UUID of the invitation

    Returns:
        Invitation details
    """
    logger.info(f"Getting invitation {invitation_id} details")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/invitations/{invitation_id}")
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_invitation(organization_id: str, invitation_id: str) -> Dict[str, Any]:
    """Delete/cancel an invitation.

    Args:
        organization_id: UUID of the organization
        invitation_id: UUID of the invitation

    Returns:
        Deletion confirmation
    """
    logger.info(f"Deleting invitation {invitation_id}")
    client = create_cloud_client()
    response = client.delete(f"/v1/organizations/{organization_id}/invitations/{invitation_id}")
    return _handle_api_response(response)


# Backup Tools
@mcp.tool()
def cloud_list_backups(organization_id: str, service_id: str) -> Dict[str, Any]:
    """List all backups for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        List of backups (most recent first)
    """
    logger.info(f"Listing backups for service {service_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}/backups")
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_backup(organization_id: str, service_id: str, backup_id: str) -> Dict[str, Any]:
    """Get details of a specific backup.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        backup_id: UUID of the backup

    Returns:
        Backup details including status, size, and duration
    """
    logger.info(f"Getting backup {backup_id} details")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/backups/{backup_id}"
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_backup_configuration(organization_id: str, service_id: str) -> Dict[str, Any]:
    """Get backup configuration for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        Backup configuration settings
    """
    logger.info(f"Getting backup configuration for service {service_id}")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/backupConfiguration"
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_backup_configuration(
    organization_id: str,
    service_id: str,
    backup_period_in_hours: Optional[int] = None,
    backup_retention_period_in_hours: Optional[int] = None,
    backup_start_time: Optional[str] = None,
) -> Dict[str, Any]:
    """Update backup configuration for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        backup_period_in_hours: Interval between backups in hours
        backup_retention_period_in_hours: How long to keep backups in hours
        backup_start_time: Daily backup time in HH:MM format (UTC)

    Returns:
        Updated backup configuration
    """
    logger.info(f"Updating backup configuration for service {service_id}")
    client = create_cloud_client()

    data = {}
    if backup_period_in_hours is not None:
        data["backupPeriodInHours"] = backup_period_in_hours
    if backup_retention_period_in_hours is not None:
        data["backupRetentionPeriodInHours"] = backup_retention_period_in_hours
    if backup_start_time is not None:
        data["backupStartTime"] = backup_start_time

    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/backupConfiguration", data=data
    )
    return _handle_api_response(response)


# Activity Log Tools
@mcp.tool()
def cloud_list_activities(
    organization_id: str, from_date: Optional[str] = None, to_date: Optional[str] = None
) -> Dict[str, Any]:
    """List organization activities (audit log).

    Args:
        organization_id: UUID of the organization
        from_date: Start date for activity search (ISO-8601)
        to_date: End date for activity search (ISO-8601)

    Returns:
        List of organization activities
    """
    logger.info(f"Listing activities for organization {organization_id}")
    client = create_cloud_client()

    params = {}
    if from_date is not None:
        params["from_date"] = from_date
    if to_date is not None:
        params["to_date"] = to_date

    response = client.get(f"/v1/organizations/{organization_id}/activities", params=params)
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_activity(organization_id: str, activity_id: str) -> Dict[str, Any]:
    """Get details of a specific activity.

    Args:
        organization_id: UUID of the organization
        activity_id: ID of the activity

    Returns:
        Activity details
    """
    logger.info(f"Getting activity {activity_id} details")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/activities/{activity_id}")
    return _handle_api_response(response)


# Usage and Cost Tools
@mcp.tool()
def cloud_get_usage_cost(organization_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
    """Get organization usage costs for a date range.

    Args:
        organization_id: UUID of the organization
        from_date: Start date (YYYY-MM-DD format)
        to_date: End date (YYYY-MM-DD format, max 31 days from start)

    Returns:
        Usage cost data with grand total and per-entity breakdown
    """
    logger.info(
        f"Getting usage costs for organization {organization_id} from {from_date} to {to_date}"
    )
    client = create_cloud_client()

    params = {"from_date": from_date, "to_date": to_date}

    response = client.get(f"/v1/organizations/{organization_id}/usageCost", params=params)
    return _handle_api_response(response)


# Private Endpoint Tools
@mcp.tool()
def cloud_get_private_endpoint_config(organization_id: str, service_id: str) -> Dict[str, Any]:
    """Get private endpoint configuration for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        Private endpoint configuration details
    """
    logger.info(f"Getting private endpoint config for service {service_id}")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/privateEndpointConfig"
    )
    return _handle_api_response(response)


# Reverse Private Endpoints (Beta)
@mcp.tool()
def cloud_list_reverse_private_endpoints(organization_id: str, service_id: str) -> Dict[str, Any]:
    """List all reverse private endpoints for a service (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        List of reverse private endpoints
    """
    logger.info(f"Listing reverse private endpoints for service {service_id}")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/reversePrivateEndpoints"
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_reverse_private_endpoint(
    organization_id: str,
    service_id: str,
    description: str,
    type: str,
    vpc_endpoint_service_name: Optional[str] = None,
    vpc_resource_configuration_id: Optional[str] = None,
    vpc_resource_share_arn: Optional[str] = None,
    msk_cluster_arn: Optional[str] = None,
    msk_authentication: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new reverse private endpoint (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        description: Reverse private endpoint description (max 255 chars)
        type: Reverse private endpoint type (VPC_ENDPOINT_SERVICE, VPC_RESOURCE, MSK_MULTI_VPC)
        vpc_endpoint_service_name: VPC endpoint service name
        vpc_resource_configuration_id: VPC resource configuration ID (required for VPC_RESOURCE)
        vpc_resource_share_arn: VPC resource share ARN (required for VPC_RESOURCE)
        msk_cluster_arn: MSK cluster ARN (required for MSK_MULTI_VPC)
        msk_authentication: MSK authentication type (SASL_IAM, SASL_SCRAM)

    Returns:
        Created reverse private endpoint details
    """
    logger.info(f"Creating reverse private endpoint for service {service_id}")
    client = create_cloud_client()

    data = {"description": description, "type": type}

    if vpc_endpoint_service_name is not None:
        data["vpcEndpointServiceName"] = vpc_endpoint_service_name
    if vpc_resource_configuration_id is not None:
        data["vpcResourceConfigurationId"] = vpc_resource_configuration_id
    if vpc_resource_share_arn is not None:
        data["vpcResourceShareArn"] = vpc_resource_share_arn
    if msk_cluster_arn is not None:
        data["mskClusterArn"] = msk_cluster_arn
    if msk_authentication is not None:
        data["mskAuthentication"] = msk_authentication

    response = client.post(
        f"/v1/organizations/{organization_id}/services/{service_id}/reversePrivateEndpoints",
        data=data,
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_reverse_private_endpoint(
    organization_id: str, service_id: str, reverse_private_endpoint_id: str
) -> Dict[str, Any]:
    """Get details of a specific reverse private endpoint (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        reverse_private_endpoint_id: UUID of the reverse private endpoint

    Returns:
        Reverse private endpoint details
    """
    logger.info(f"Getting reverse private endpoint {reverse_private_endpoint_id} details")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/reversePrivateEndpoints/{reverse_private_endpoint_id}"
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_reverse_private_endpoint(
    organization_id: str, service_id: str, reverse_private_endpoint_id: str
) -> Dict[str, Any]:
    """Delete a reverse private endpoint (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        reverse_private_endpoint_id: UUID of the reverse private endpoint

    Returns:
        Deletion confirmation
    """
    logger.info(f"Deleting reverse private endpoint {reverse_private_endpoint_id}")
    client = create_cloud_client()
    response = client.delete(
        f"/v1/organizations/{organization_id}/services/{service_id}/reversePrivateEndpoints/{reverse_private_endpoint_id}"
    )
    return _handle_api_response(response)


# ClickPipes Tools (Beta)
@mcp.tool()
def cloud_list_clickpipes(organization_id: str, service_id: str) -> Dict[str, Any]:
    """List all ClickPipes for a service.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service

    Returns:
        List of ClickPipes
    """
    logger.info(f"Listing ClickPipes for service {service_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes")
    return _handle_api_response(response)


@mcp.tool()
def cloud_create_clickpipe(
    organization_id: str,
    service_id: str,
    name: str,
    description: str,
    source: Dict,
    destination: Dict,
    field_mappings: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Create a new ClickPipe (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        name: Name of the ClickPipe
        description: Description of the ClickPipe
        source: Source configuration (kafka, objectStorage, kinesis, postgres)
        destination: Destination configuration
        field_mappings: Field mappings of the ClickPipe

    Returns:
        Created ClickPipe details
    """
    logger.info(f"Creating ClickPipe {name} for service {service_id}")
    client = create_cloud_client()

    data = {"name": name, "description": description, "source": source, "destination": destination}

    if field_mappings is not None:
        data["fieldMappings"] = field_mappings

    response = client.post(
        f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes", data=data
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_clickpipe(organization_id: str, service_id: str, clickpipe_id: str) -> Dict[str, Any]:
    """Get details of a specific ClickPipe.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        clickpipe_id: UUID of the ClickPipe

    Returns:
        ClickPipe details including source, destination, and state
    """
    logger.info(f"Getting ClickPipe {clickpipe_id} details")
    client = create_cloud_client()
    response = client.get(
        f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}"
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_clickpipe(
    organization_id: str,
    service_id: str,
    clickpipe_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    source: Optional[Dict] = None,
    destination: Optional[Dict] = None,
    field_mappings: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """Update a ClickPipe (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        clickpipe_id: UUID of the ClickPipe
        name: Name of the ClickPipe
        description: Description of the ClickPipe
        source: Source configuration updates
        destination: Destination configuration updates
        field_mappings: Field mappings updates

    Returns:
        Updated ClickPipe details
    """
    logger.info(f"Updating ClickPipe {clickpipe_id}")
    client = create_cloud_client()

    data = {}
    if name is not None:
        data["name"] = name
    if description is not None:
        data["description"] = description
    if source is not None:
        data["source"] = source
    if destination is not None:
        data["destination"] = destination
    if field_mappings is not None:
        data["fieldMappings"] = field_mappings

    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}",
        data=data,
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_clickpipe_scaling(
    organization_id: str, service_id: str, clickpipe_id: str, replicas: Optional[int] = None
) -> Dict[str, Any]:
    """Update ClickPipe scaling settings (beta).

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        clickpipe_id: UUID of the ClickPipe
        replicas: Number of replicas to scale to (1-10, for Kafka pipes)

    Returns:
        Updated ClickPipe details
    """
    logger.info(f"Updating ClickPipe {clickpipe_id} scaling")
    client = create_cloud_client()

    data = {}
    if replicas is not None:
        data["replicas"] = replicas

    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}/scaling",
        data=data,
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_clickpipe_state(
    organization_id: str, service_id: str, clickpipe_id: str, command: str
) -> Dict[str, Any]:
    """Start, stop, or resync a ClickPipe.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        clickpipe_id: UUID of the ClickPipe
        command: Command to execute (start, stop, resync)

    Returns:
        Updated ClickPipe details
    """
    logger.info(f"Updating ClickPipe {clickpipe_id} state: {command}")
    client = create_cloud_client()

    data = {"command": command}
    response = client.patch(
        f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}/state",
        data=data,
    )
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_clickpipe(
    organization_id: str, service_id: str, clickpipe_id: str
) -> Dict[str, Any]:
    """Delete a ClickPipe.

    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        clickpipe_id: UUID of the ClickPipe

    Returns:
        Deletion confirmation
    """
    logger.info(f"Deleting ClickPipe {clickpipe_id}")
    client = create_cloud_client()
    response = client.delete(
        f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}"
    )
    return _handle_api_response(response)


# Utility Tools
@mcp.tool()
def cloud_get_available_regions() -> Dict[str, Any]:
    """Get information about available cloud regions.

    Returns:
        Information about supported regions and providers
    """
    logger.info("Getting available regions information")

    # This is static information from the API spec
    regions_info = {
        "aws": [
            "ap-south-1",
            "ap-southeast-1",
            "ap-southeast-2",
            "ap-northeast-1",
            "eu-central-1",
            "eu-west-1",
            "eu-west-2",
            "us-east-1",
            "us-east-2",
            "us-west-2",
            "me-central-1",
        ],
        "gcp": ["us-east1", "us-central1", "europe-west4", "asia-southeast1"],
        "azure": ["eastus", "eastus2", "westus3", "germanywestcentral"],
    }

    return {
        "status": "success",
        "data": {
            "providers": list(regions_info.keys()),
            "regions": regions_info,
            "total_regions": sum(len(regions) for regions in regions_info.values()),
        },
    }
