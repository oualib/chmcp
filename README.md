# MCP ClickHouse: Database Operations + Cloud Management

[![PyPI - Version](https://img.shields.io/pypi/v/chmcp)](https://pypi.org/project/chmcp)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A comprehensive Model Context Protocol (MCP) server that provides **two distinct capabilities**:
1. **Database Operations** - Connect to and query any ClickHouse database (local, cloud, or self-hosted)
2. **Cloud Management** - Complete ClickHouse Cloud infrastructure management via API

## 🚀 Quick Start

Start with our step-by-step tutorial:

👉 **[Complete Setup Tutorial](tutorial/README.md)** - Transform Claude into a powerful ClickHouse data agent

For experienced users, jump to the [Quick Configuration](#quick-configuration) section below.

## 📚 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [📚 Table of Contents](#-table-of-contents)
- [🎯 Choose Your Use Case](#-choose-your-use-case)
- [🌟 Why This Server?](#-why-this-server)
- [✨ Capabilities Overview](#-capabilities-overview)
- [⚡ Quick Configuration](#-quick-configuration)
- [📦 Installation](#-installation)
- [⚙️ Configuration Guide](#️-configuration-guide)
- [🛠️ Available Tools](#️-available-tools)
- [💡 Usage Examples](#-usage-examples)
- [🔧 Development](#-development)
- [🐛 Troubleshooting](#-troubleshooting)
- [📄 License](#-license)

## 🎯 Choose Your Use Case

This MCP server supports two independent use cases. You can use one or both:

### 📊 Database Operations Only
**For:** Data analysis, querying, and exploration of ClickHouse databases
- Connect to any ClickHouse instance (local, self-hosted, or ClickHouse Cloud)
- Execute read-only queries safely
- Explore database schemas and metadata
- **Setup:** Database connection credentials only

### ☁️ Cloud Management Only  
**For:** Managing ClickHouse Cloud infrastructure programmatically
- Create, configure, and manage cloud services
- Handle API keys, members, and organizations
- Monitor usage, costs, and performance
- **Setup:** ClickHouse Cloud API keys only

### 🔄 Both Combined
**For:** Complete ClickHouse workflow from infrastructure to data
- Manage cloud services AND query the databases within them
- End-to-end data pipeline management
- **Setup:** Both database credentials and cloud API keys

## 🌟 Why This Server?

This repository significantly improves over the [original ClickHouse MCP server](https://github.com/ClickHouse/mcp-clickhouse):

| Feature | Original Server | This Server |
|---------|----------------|-------------|
| **Database Operations** | 3 basic tools | 3 enhanced tools with safety features |
| **Cloud Management** | ❌ None | ✅ 50+ comprehensive tools (100% API coverage) |
| **Code Quality** | Basic | Production-ready with proper structure |
| **Configuration** | Limited options | Flexible setup for any use case |
| **Error Handling** | Basic | Robust with detailed error messages |
| **SSL Support** | Limited | Full SSL configuration options |

## ✨ Capabilities Overview

### 📊 Database Operations (3 Tools)
Connect to and query any ClickHouse database:
- **List databases and tables** with detailed metadata
- **Execute SELECT queries** with safety guarantees (read-only mode)
- **Explore schemas** including column types, row counts, and table structures
- **Works with:** Local ClickHouse, self-hosted instances, ClickHouse Cloud databases, and the free SQL Playground

### ☁️ Cloud Management (50+ Tools)
Complete ClickHouse Cloud API integration:
- **Organizations** (5 tools): Manage settings, metrics, private endpoints
- **Services** (12 tools): Create, scale, start/stop, configure, delete cloud services
- **API Keys** (5 tools): Full CRUD operations for programmatic access
- **Members & Invitations** (8 tools): User management and access control
- **Backups** (4 tools): Configure and manage automated backups
- **ClickPipes** (7 tools): Data ingestion pipeline management
- **Monitoring** (3 tools): Usage analytics, costs, and audit logs
- **Network** (6 tools): Private endpoints and security configuration

## ⚡ Quick Configuration

### Claude Desktop Setup

1. Open your Claude Desktop configuration file:
   * **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   * **Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

2. Choose your configuration based on your use case:

<details>
<summary><strong>📊 Database Operations Only</strong> (Click to expand)</summary>

#### For Your Own ClickHouse Server
```json
{
  "mcpServers": {
    "chmcp": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "chmcp", "--python", "3.13", "chmcp"],
      "env": {
        "CLICKHOUSE_HOST": "your-server.com",
        "CLICKHOUSE_PORT": "8443",
        "CLICKHOUSE_USER": "your-username",
        "CLICKHOUSE_PASSWORD": "your-password",
        "CLICKHOUSE_SECURE": "true"
      }
    }
  }
}
```

#### For ClickHouse Cloud Database
```json
{
  "mcpServers": {
    "chmcp": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "chmcp", "--python", "3.13", "chmcp"],
      "env": {
        "CLICKHOUSE_HOST": "your-instance.clickhouse.cloud",
        "CLICKHOUSE_USER": "default",
        "CLICKHOUSE_PASSWORD": "your-database-password",
        "CLICKHOUSE_SECURE": "true"
      }
    }
  }
}
```

#### For Free Testing (SQL Playground)
```json
{
  "mcpServers": {
    "chmcp": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "chmcp", "--python", "3.13", "chmcp"],
      "env": {
        "CLICKHOUSE_HOST": "sql-clickhouse.clickhouse.com",
        "CLICKHOUSE_PORT": "8443",
        "CLICKHOUSE_USER": "demo",
        "CLICKHOUSE_PASSWORD": "",
        "CLICKHOUSE_SECURE": "true"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>☁️ Cloud Management Only</strong> (Click to expand)</summary>

```json
{
  "mcpServers": {
    "chmcp": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "chmcp", "--python", "3.13", "chmcp"],
      "env": {
        "CLICKHOUSE_CLOUD_KEY_ID": "your-cloud-key-id",
        "CLICKHOUSE_CLOUD_KEY_SECRET": "your-cloud-key-secret"
      }
    }
  }
}
```
</details>

<details>
<summary><strong>🔄 Both Database + Cloud Management</strong> (Click to expand)</summary>

```json
{
  "mcpServers": {
    "chmcp": {
      "command": "/path/to/uv",
      "args": ["run", "--with", "chmcp", "--python", "3.13", "chmcp"],
      "env": {
        "CLICKHOUSE_HOST": "your-instance.clickhouse.cloud",
        "CLICKHOUSE_USER": "default",
        "CLICKHOUSE_PASSWORD": "your-database-password",
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_CLOUD_KEY_ID": "your-cloud-key-id",
        "CLICKHOUSE_CLOUD_KEY_SECRET": "your-cloud-key-secret"
      }
    }
  }
}
```
</details>

3. **Important:** Replace `/path/to/uv` with the absolute path to your `uv` executable (find it with `which uv` on macOS/Linux)

4. **Restart Claude Desktop** to apply the changes

## 📦 Installation

### Option 1: Using uv (Recommended)
```bash
# Install via uv (used by Claude Desktop)
uv add chmcp
```

### Option 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/oualib/chmcp.git
cd chmcp

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## ⚙️ Configuration Guide

### 📊 Database Configuration

Set these environment variables to enable database operations:

#### Required Variables
```bash
CLICKHOUSE_HOST=your-clickhouse-host.com    # ClickHouse server hostname
CLICKHOUSE_USER=your-username               # Username for authentication
CLICKHOUSE_PASSWORD=your-password           # Password for authentication
```

#### Optional Variables (with defaults)
```bash
CLICKHOUSE_PORT=8443                        # 8443 for HTTPS, 8123 for HTTP
CLICKHOUSE_SECURE=true                      # Enable HTTPS connection
CLICKHOUSE_VERIFY=true                      # Verify SSL certificates
CLICKHOUSE_CONNECT_TIMEOUT=30               # Connection timeout in seconds
CLICKHOUSE_SEND_RECEIVE_TIMEOUT=300         # Query timeout in seconds
CLICKHOUSE_DATABASE=default                 # Default database to use
```

> [!CAUTION]
> **Security Best Practice:** Create a dedicated database user with minimal privileges for MCP connections. Avoid using administrative accounts.

### ☁️ Cloud API Configuration

Set these environment variables to enable cloud management:

#### Required Variables
```bash
CLICKHOUSE_CLOUD_KEY_ID=your-cloud-key-id          # From ClickHouse Cloud Console
CLICKHOUSE_CLOUD_KEY_SECRET=your-cloud-key-secret  # From ClickHouse Cloud Console
```

#### Optional Variables (with defaults)
```bash
CLICKHOUSE_CLOUD_API_URL=https://api.clickhouse.cloud   # API endpoint
CLICKHOUSE_CLOUD_TIMEOUT=30                             # Request timeout
CLICKHOUSE_CLOUD_SSL_VERIFY=true                        # SSL verification
```

### 🔑 Getting ClickHouse Cloud API Keys

1. Log into [ClickHouse Cloud Console](https://console.clickhouse.cloud/)
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Select appropriate permissions:
   - **Admin**: Full access to all resources
   - **Developer**: Service and resource management
   - **Query Endpoints**: Limited to query operations
5. Copy the **Key ID** and **Key Secret** to your configuration

### Example Configurations

<details>
<summary><strong>Local Development with Docker</strong></summary>

```env
# Database only
CLICKHOUSE_HOST=localhost
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=clickhouse
CLICKHOUSE_SECURE=false
CLICKHOUSE_PORT=8123
```
</details>

<details>
<summary><strong>ClickHouse Cloud (Database + Management)</strong></summary>

```env
# Database connection
CLICKHOUSE_HOST=your-instance.clickhouse.cloud
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your-database-password
CLICKHOUSE_SECURE=true

# Cloud management
CLICKHOUSE_CLOUD_KEY_ID=your-cloud-key-id
CLICKHOUSE_CLOUD_KEY_SECRET=your-cloud-key-secret
```
</details>

<details>
<summary><strong>SSL Issues Troubleshooting</strong></summary>

If you encounter SSL certificate verification issues:

```env
# Disable SSL verification for database
CLICKHOUSE_VERIFY=false

# Disable SSL verification for cloud API
CLICKHOUSE_CLOUD_SSL_VERIFY=false
```
</details>

## 🛠️ Available Tools

### 📊 Database Tools (3 tools)

These tools work with any ClickHouse database when database configuration is provided:

- **`list_databases()`** - List all available databases
- **`list_tables(database, like?, not_like?)`** - List tables with detailed metadata including schema, row counts, and column information
- **`run_select_query(query)`** - Execute SELECT queries safely (all queries run with `readonly = 1` for security)

### ☁️ Cloud Management Tools (50+ tools)

These tools work with ClickHouse Cloud when API credentials are provided:

#### Organization Management (5 tools)
- `cloud_list_organizations()` - List available organizations
- `cloud_get_organization(organization_id)` - Get organization details
- `cloud_update_organization(organization_id, name?, private_endpoints?)` - Update organization settings
- `cloud_get_organization_metrics(organization_id, filtered_metrics?)` - Get Prometheus metrics
- `cloud_get_organization_private_endpoint_info(organization_id, cloud_provider, region)` - Get private endpoint information

#### Service Management (12 tools)
- `cloud_list_services(organization_id)` - List all services in organization
- `cloud_get_service(organization_id, service_id)` - Get detailed service information
- `cloud_create_service(organization_id, name, provider, region, ...)` - Create new service with full configuration options
- `cloud_update_service(organization_id, service_id, ...)` - Update service settings
- `cloud_update_service_state(organization_id, service_id, command)` - Start/stop services
- `cloud_update_service_scaling(organization_id, service_id, ...)` - Configure auto-scaling (legacy method)
- `cloud_update_service_replica_scaling(organization_id, service_id, ...)` - Configure replica-based scaling (preferred)
- `cloud_update_service_password(organization_id, service_id, ...)` - Update service password
- `cloud_create_service_private_endpoint(organization_id, service_id, id, description)` - Create private endpoint
- `cloud_get_service_metrics(organization_id, service_id, filtered_metrics?)` - Get service performance metrics
- `cloud_delete_service(organization_id, service_id)` - Delete service (must be stopped first)

#### API Key Management (5 tools)
- `cloud_list_api_keys(organization_id)` - List all API keys
- `cloud_create_api_key(organization_id, name, roles, ...)` - Create new API key with permissions
- `cloud_get_api_key(organization_id, key_id)` - Get API key details
- `cloud_update_api_key(organization_id, key_id, ...)` - Update API key properties
- `cloud_delete_api_key(organization_id, key_id)` - Delete API key

#### User Management (8 tools)
- `cloud_list_members(organization_id)` - List organization members
- `cloud_get_member(organization_id, user_id)` - Get member details
- `cloud_update_member_role(organization_id, user_id, role)` - Update member role
- `cloud_remove_member(organization_id, user_id)` - Remove member from organization
- `cloud_list_invitations(organization_id)` - List pending invitations
- `cloud_create_invitation(organization_id, email, role)` - Send invitation to join organization
- `cloud_get_invitation(organization_id, invitation_id)` - Get invitation details
- `cloud_delete_invitation(organization_id, invitation_id)` - Cancel pending invitation

#### Backup Management (4 tools)
- `cloud_list_backups(organization_id, service_id)` - List service backups
- `cloud_get_backup(organization_id, service_id, backup_id)` - Get backup details and status
- `cloud_get_backup_configuration(organization_id, service_id)` - Get backup configuration
- `cloud_update_backup_configuration(organization_id, service_id, ...)` - Update backup settings

#### Data Pipeline Management (7 tools - Beta)
- `cloud_list_clickpipes(organization_id, service_id)` - List ClickPipes for data ingestion
- `cloud_create_clickpipe(organization_id, service_id, name, description, source, destination, field_mappings?)` - Create data ingestion pipeline
- `cloud_get_clickpipe(organization_id, service_id, clickpipe_id)` - Get ClickPipe details and status
- `cloud_update_clickpipe(organization_id, service_id, clickpipe_id, ...)` - Update ClickPipe configuration
- `cloud_update_clickpipe_scaling(organization_id, service_id, clickpipe_id, replicas?)` - Scale ClickPipe processing
- `cloud_update_clickpipe_state(organization_id, service_id, clickpipe_id, command)` - Start/stop/resync ClickPipe
- `cloud_delete_clickpipe(organization_id, service_id, clickpipe_id)` - Delete ClickPipe

#### Network & Security (6 tools)
- `cloud_get_private_endpoint_config(organization_id, service_id)` - Get private endpoint configuration
- `cloud_list_reverse_private_endpoints(organization_id, service_id)` - List reverse private endpoints (Beta)
- `cloud_create_reverse_private_endpoint(organization_id, service_id, description, type, ...)` - Create reverse private endpoint (Beta)
- `cloud_get_reverse_private_endpoint(organization_id, service_id, reverse_private_endpoint_id)` - Get reverse private endpoint details (Beta)
- `cloud_delete_reverse_private_endpoint(organization_id, service_id, reverse_private_endpoint_id)` - Delete reverse private endpoint (Beta)
- `cloud_get_available_regions()` - Get supported cloud regions and providers

#### Monitoring & Analytics (3 tools)
- `cloud_list_activities(organization_id, from_date?, to_date?)` - Get audit logs and activity history
- `cloud_get_activity(organization_id, activity_id)` - Get detailed activity information
- `cloud_get_usage_cost(organization_id, from_date, to_date)` - Get detailed usage and cost analytics

#### Query Endpoints (3 tools - Experimental)
- `cloud_get_query_endpoint_config(organization_id, service_id)` - Get query endpoint configuration
- `cloud_create_query_endpoint_config(organization_id, service_id, roles, open_api_keys, allowed_origins)` - Create query endpoint configuration
- `cloud_delete_query_endpoint_config(organization_id, service_id)` - Delete query endpoint configuration

## 💡 Usage Examples

### 📊 Database Operations Examples

```python
# Explore database structure
databases = list_databases()
print(f"Available databases: {[db['name'] for db in databases]}")

# Get detailed table information
tables = list_tables("my_database")
for table in tables:
    print(f"Table: {table['name']}, Rows: {table['total_rows']}")

# Execute analytical queries
result = run_select_query("""
    SELECT 
        date_trunc('day', timestamp) as day,
        count(*) as events,
        avg(value) as avg_value
    FROM my_table 
    WHERE timestamp >= '2024-01-01'
    GROUP BY day
    ORDER BY day
""")
```

### ☁️ Cloud Management Examples

```python
# List all organizations and services
orgs = cloud_list_organizations()
for org in orgs:
    services = cloud_list_services(org['id'])
    print(f"Organization: {org['name']}, Services: {len(services)}")

# Create a production service with full configuration
service = cloud_create_service(
    organization_id="org-123",
    name="analytics-prod",
    provider="aws",
    region="us-east-1",
    tier="production",
    min_replica_memory_gb=32,
    max_replica_memory_gb=256,
    num_replicas=3,
    idle_scaling=True,
    idle_timeout_minutes=10,
    ip_access_list=[
        {"source": "10.0.0.0/8", "description": "Internal network"},
        {"source": "203.0.113.0/24", "description": "Office network"}
    ]
)

# Start the service and monitor status
cloud_update_service_state(
    organization_id="org-123",
    service_id=service['id'],
    command="start"
)

# Set up automated backups
cloud_update_backup_configuration(
    organization_id="org-123",
    service_id=service['id'],
    backup_period_in_hours=24,
    backup_retention_period_in_hours=168,  # 7 days
    backup_start_time="02:00"
)
```

### 🔄 Combined Workflow Example

```python
# 1. Create cloud infrastructure
service = cloud_create_service(
    organization_id="org-123",
    name="data-pipeline",
    provider="aws",
    region="us-west-2"
)

# 2. Wait for service to be ready, then connect to database
# (Once service is running, use its hostname for database connection)

# 3. Set up data ingestion pipeline
clickpipe = cloud_create_clickpipe(
    organization_id="org-123",
    service_id=service['id'],
    name="kafka-events",
    description="Real-time event ingestion",
    source={
        "kafka": {
            "type": "kafka",
            "format": "JSONEachRow",
            "brokers": "kafka.example.com:9092",
            "topics": "user-events",
            "authentication": "SASL_SSL"
        }
    },
    destination={
        "database": "analytics",
        "table": "events",
        "managedTable": True
    }
)

# 4. Query the ingested data
result = run_select_query("""
    SELECT 
        event_type,
        count(*) as event_count,
        uniq(user_id) as unique_users
    FROM analytics.events
    WHERE timestamp >= now() - INTERVAL 1 HOUR
    GROUP BY event_type
    ORDER BY event_count DESC
""")
```

## 🔧 Development

### Local Development Setup

1. **Start ClickHouse for testing**:
   ```bash
   cd test-services
   docker compose up -d
   ```

2. **Create environment file**:
   ```bash
   cat > .env << EOF
   # Database configuration
   CLICKHOUSE_HOST=localhost
   CLICKHOUSE_PORT=8123
   CLICKHOUSE_USER=default
   CLICKHOUSE_PASSWORD=clickhouse
   CLICKHOUSE_SECURE=false
   
   # Cloud configuration (optional)
   CLICKHOUSE_CLOUD_KEY_ID=your-key-id
   CLICKHOUSE_CLOUD_KEY_SECRET=your-key-secret
   EOF
   ```

3. **Install and run**:
   ```bash
   uv sync                               # Install dependencies
   source .venv/bin/activate            # Activate virtual environment
   mcp dev chmcp/mcp_server.py          # Start for testing
   # OR
   python -m chmcp.main                 # Start normally
   ```

### Project Structure

```
chmcp/
├── __init__.py                 # Package initialization
├── main.py                     # Entry point
├── mcp_env.py                  # Database environment configuration
├── mcp_server.py              # Main server + database tools (3 tools)
├── cloud_config.py            # Cloud API configuration
├── cloud_client.py            # HTTP client for Cloud API
└── cloud_tools.py             # Cloud MCP tools (50+ tools)
```

### Running Tests

```bash
uv sync --all-extras --dev              # Install dev dependencies
uv run ruff check .                     # Run linting
docker compose up -d                    # Start test ClickHouse
uv run pytest tests                     # Run tests
```

## 🐛 Troubleshooting

### 📊 Database Connection Issues

**Problem:** Can't connect to ClickHouse database
- ✅ Verify `CLICKHOUSE_HOST`, `CLICKHOUSE_USER`, and `CLICKHOUSE_PASSWORD`
- ✅ Test network connectivity: `telnet your-host 8443`
- ✅ Check firewall settings allow connections on the specified port
- ✅ For SSL issues, try setting `CLICKHOUSE_VERIFY=false`
- ✅ Ensure database user has appropriate SELECT permissions

**Problem:** SSL certificate verification fails
```bash
# Temporarily disable SSL verification
CLICKHOUSE_VERIFY=false
CLICKHOUSE_SECURE=false  # Use HTTP instead of HTTPS
CLICKHOUSE_PORT=8123     # HTTP port instead of 8443
```

### ☁️ Cloud API Issues

**Problem:** Cloud tools not working
- ✅ Verify `CLICKHOUSE_CLOUD_KEY_ID` and `CLICKHOUSE_CLOUD_KEY_SECRET` are correct
- ✅ Check API key permissions in ClickHouse Cloud Console
- ✅ Ensure API key is active and not expired
- ✅ For SSL issues, try setting `CLICKHOUSE_CLOUD_SSL_VERIFY=false`

**Problem:** "Organization not found" errors
- ✅ List organizations first: `cloud_list_organizations()`
- ✅ Verify your API key has access to the organization
- ✅ Check that you're using the correct organization ID format

### 🔧 General Issues

**Problem:** Tools missing in Claude
- ✅ Database tools require database configuration (`CLICKHOUSE_HOST`, etc.)
- ✅ Cloud tools require API configuration (`CLICKHOUSE_CLOUD_KEY_ID`, etc.)
- ✅ Check Claude Desktop configuration file syntax
- ✅ Restart Claude Desktop after configuration changes
- ✅ Verify `uv` path is absolute in configuration

**Problem:** Import errors or missing dependencies
```bash
# Reinstall with latest dependencies
uv sync --force
# Or manual installation
pip install -r requirements.txt --force-reinstall
```

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

**Developed by [Badr Ouali](https://github.com/oualib)**