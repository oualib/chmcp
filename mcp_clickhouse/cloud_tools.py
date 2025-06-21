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
            "request_id": response.request_id
        }
    
    return {
        "status": "success",
        "data": response.result,
        "status_code": response.status,
        "request_id": response.request_id
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
def cloud_update_organization(organization_id: str, name: Optional[str] = None) -> Dict[str, Any]:
    """Update organization details.
    
    Args:
        organization_id: UUID of the organization
        name: New organization name
        
    Returns:
        Updated organization details
    """
    logger.info(f"Updating organization {organization_id}")
    client = create_cloud_client()
    
    data = {}
    if name is not None:
        data["name"] = name
    
    response = client.patch(f"/v1/organizations/{organization_id}", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_get_organization_metrics(organization_id: str, filtered_metrics: Optional[bool] = None) -> Dict[str, Any]:
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
    ip_access_list: Optional[List[Dict[str, str]]] = None
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
        "idleScaling": idle_scaling
    }
    
    if idle_timeout_minutes is not None:
        data["idleTimeoutMinutes"] = idle_timeout_minutes
    
    if ip_access_list is not None:
        data["ipAccessList"] = ip_access_list
    
    response = client.post(f"/v1/organizations/{organization_id}/services", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_service_state(organization_id: str, service_id: str, command: str) -> Dict[str, Any]:
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
    response = client.patch(f"/v1/organizations/{organization_id}/services/{service_id}/state", data=data)
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
    ip_access_list: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """Create a new API key.
    
    Args:
        organization_id: UUID of the organization
        name: Key name
        roles: List of roles (admin, developer, query_endpoints)
        expire_at: Expiration timestamp in ISO-8601 format (optional)
        state: Initial state (enabled, disabled)
        ip_access_list: List of IP access entries [{"source": "IP/CIDR", "description": "desc"}]
        
    Returns:
        Created API key details and credentials (keyId and keySecret)
    """
    logger.info(f"Creating API key {name} in organization {organization_id}")
    client = create_cloud_client()
    
    data = {
        "name": name,
        "roles": roles,
        "state": state
    }
    
    if expire_at is not None:
        data["expireAt"] = expire_at
    
    if ip_access_list is not None:
        data["ipAccessList"] = ip_access_list
    
    response = client.post(f"/v1/organizations/{organization_id}/keys", data=data)
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
    
    data = {
        "email": email,
        "role": role
    }
    
    response = client.post(f"/v1/organizations/{organization_id}/invitations", data=data)
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
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}/backups/{backup_id}")
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
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}/backupConfiguration")
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_backup_configuration(
    organization_id: str,
    service_id: str,
    backup_period_in_hours: Optional[int] = None,
    backup_retention_period_in_hours: Optional[int] = None,
    backup_start_time: Optional[str] = None
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
    
    response = client.patch(f"/v1/organizations/{organization_id}/services/{service_id}/backupConfiguration", data=data)
    return _handle_api_response(response)


# Activity Log Tools
@mcp.tool()
def cloud_list_activities(
    organization_id: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None
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
def cloud_get_usage_cost(
    organization_id: str,
    from_date: str,
    to_date: str
) -> Dict[str, Any]:
    """Get organization usage costs for a date range.
    
    Args:
        organization_id: UUID of the organization
        from_date: Start date (YYYY-MM-DD format)
        to_date: End date (YYYY-MM-DD format, max 31 days from start)
        
    Returns:
        Usage cost data with grand total and per-entity breakdown
    """
    logger.info(f"Getting usage costs for organization {organization_id} from {from_date} to {to_date}")
    client = create_cloud_client()
    
    params = {
        "from_date": from_date,
        "to_date": to_date
    }
    
    response = client.get(f"/v1/organizations/{organization_id}/usageCost", params=params)
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
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}")
    return _handle_api_response(response)


@mcp.tool()
def cloud_update_clickpipe_state(
    organization_id: str,
    service_id: str,
    clickpipe_id: str,
    command: str
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
    response = client.patch(f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}/state", data=data)
    return _handle_api_response(response)


@mcp.tool()
def cloud_delete_clickpipe(organization_id: str, service_id: str, clickpipe_id: str) -> Dict[str, Any]:
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
    response = client.delete(f"/v1/organizations/{organization_id}/services/{service_id}/clickpipes/{clickpipe_id}")
    return _handle_api_response(response)


# Private Endpoint Tools
@mcp.tool()
def cloud_get_private_endpoint_config(
    organization_id: str,
    service_id: str
) -> Dict[str, Any]:
    """Get private endpoint configuration for a service.
    
    Args:
        organization_id: UUID of the organization
        service_id: UUID of the service
        
    Returns:
        Private endpoint configuration details
    """
    logger.info(f"Getting private endpoint config for service {service_id}")
    client = create_cloud_client()
    response = client.get(f"/v1/organizations/{organization_id}/services/{service_id}/privateEndpointConfig")
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
            "ap-south-1", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
            "eu-central-1", "eu-west-1", "eu-west-2", 
            "us-east-1", "us-east-2", "us-west-2", "me-central-1"
        ],
        "gcp": [
            "us-east1", "us-central1", "europe-west4", "asia-southeast1"
        ],
        "azure": [
            "eastus", "eastus2", "westus3", "germanywestcentral"
        ]
    }
    
    return {
        "status": "success",
        "data": {
            "providers": list(regions_info.keys()),
            "regions": regions_info,
            "total_regions": sum(len(regions) for regions in regions_info.values())
        }
    }