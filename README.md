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
- [🔒 Safety Features](#-safety-features)
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

| Feature | Original Server (v0.1.10) | This Server |
|---------|----------------|-------------|
| **Database Operations** | 3 basic tools | 3 enhanced tools with safety features |
| **Query Security** | ❌ `run_select_query` allows ANY SQL operation | ✅ Proper query filtering and readonly mode |
| **Cloud Management** | ❌ None | ✅ 50+ comprehensive tools (100% API coverage) |
| **Safety Controls** | ❌ No protection against destructive operations | ✅ Advanced readonly modes for both database and cloud operations |
| **Code Quality** | Basic | Production-ready with proper structure |
| **Configuration** | Limited options | Flexible setup for any use case |
| **Error Handling** | Basic | Robust with detailed error messages |
| **SSL Support** | Limited | Full SSL configuration options |

> [!WARNING]
> **Security Notice:** The original ClickHouse MCP server (v0.1.10) has a critical security flaw where `run_select_query` can execute ANY SQL operation including DROP, DELETE, INSERT, etc., despite its name suggesting it only runs SELECT queries. This server implements proper query filtering and safety controls.

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

## 🔒 Safety Features

This MCP server includes comprehensive safety controls to prevent accidental data modification or infrastructure changes:

### 📊 Database Safety
- **Automatic Read-Only Mode**: All database queries run with `readonly = 1` by default
- **Query Filtering**: Only SELECT, SHOW, DESCRIBE, and EXPLAIN queries are allowed
- **Manual Override**: Set `CLICKHOUSE_READONLY=false` to enable write operations when needed

### ☁️ Cloud Management Safety
- **Protected Operations**: Destructive cloud operations (delete, stop) can be disabled
- **Safe Mode**: Set `CLICKHOUSE_CLOUD_READONLY=true` to prevent infrastructure changes
- **Audit Trail**: All operations are logged for accountability

### 🛡️ Security Best Practices
- **Minimal Privileges**: Create dedicated users with limited permissions
- **SSL by Default**: Secure connections enabled automatically
- **Environment Variables**: Sensitive credentials never hardcoded
- **Timeout Controls**: Prevent runaway queries and operations

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
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_READONLY": "true"
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
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_READONLY": "true"
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
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_READONLY": "true"
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

> **Note:** `CLICKHOUSE_CLOUD_READONLY` defaults to `false` (full access). Add `"CLICKHOUSE_CLOUD_READONLY": "true"` for monitoring-only mode.

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
        "CLICKHOUSE_READONLY": "true",
        "CLICKHOUSE_CLOUD_KEY_ID": "your-cloud-key-id",
        "CLICKHOUSE_CLOUD_KEY_SECRET": "your-cloud-key-secret"
      }
    }
  }
}
```

> **Note:** This enables database analysis (readonly) + full cloud management. Add `"CLICKHOUSE_CLOUD_READONLY": "true"` for monitoring-only mode.

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

#### Safety & Security Variables
```bash
CLICKHOUSE_READONLY=true                    # Enable read-only mode (recommended)
                                           # true: Only SELECT/SHOW/DESCRIBE queries allowed
                                           # false: All SQL operations permitted
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
> **Security Best Practice:** Always use `CLICKHOUSE_READONLY=true` in production environments. Create a dedicated database user with minimal privileges for MCP connections. Avoid using administrative accounts.

### ☁️ Cloud API Configuration

Set these environment variables to enable cloud management:

#### Required Variables
```bash
CLICKHOUSE_CLOUD_KEY_ID=your-cloud-key-id          # From ClickHouse Cloud Console
CLICKHOUSE_CLOUD_KEY_SECRET=your-cloud-key-secret  # From ClickHouse Cloud Console
```

#### Safety & Security Variables
```bash
CLICKHOUSE_CLOUD_READONLY=false            # Cloud operation mode (default: false)
                                           # true: Only read operations (list, get, metrics)
                                           # false: All cloud operations permitted (create, update, delete)
```

#### Optional Variables (with defaults)
```bash
CLICKHOUSE_CLOUD_API_URL=https://api.clickhouse.cloud   # API endpoint
CLICKHOUSE_CLOUD_TIMEOUT=30                             # Request timeout
CLICKHOUSE_CLOUD_SSL_VERIFY=true                        # SSL verification
```

> [!WARNING]
> **Cloud Safety:** By default, `CLICKHOUSE_CLOUD_READONLY=false` allows all infrastructure operations. Set to `true` in production to prevent accidental infrastructure changes. When disabled, Claude can create, modify, and delete cloud services, which may incur costs or cause service disruptions.

### 🔑 Getting ClickHouse Cloud API Keys

1. Log into [ClickHouse Cloud Console](https://console.clickhouse.cloud/)
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Select appropriate permissions:
   - **Admin**: Full access to all resources
   - **Developer**: Service and resource management
   - **Query Endpoints**: Limited to query operations
5. Copy the **Key ID** and **Key Secret** to your configuration

### 🔒 Safety Configuration Examples

<details>
<summary><strong>Production Safe Mode (Recommended)</strong></summary>

```env
# Database - read-only queries only
CLICKHOUSE_HOST=your-instance.clickhouse.cloud
CLICKHOUSE_USER=readonly_user
CLICKHOUSE_PASSWORD=secure-password
CLICKHOUSE_SECURE=true
CLICKHOUSE_READONLY=true

# Cloud - monitoring and inspection only (explicitly set to true)
CLICKHOUSE_CLOUD_KEY_ID=your-cloud-key-id
CLICKHOUSE_CLOUD_KEY_SECRET=your-cloud-key-secret
CLICKHOUSE_CLOUD_READONLY=true
```
</details>

<details>
<summary><strong>Development Mode (Full Access)</strong></summary>

```env
# Database - all operations allowed
CLICKHOUSE_HOST=localhost
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=clickhouse
CLICKHOUSE_SECURE=false
CLICKHOUSE_READONLY=false

# Cloud - full infrastructure management
CLICKHOUSE_CLOUD_KEY_ID=dev-key-id
CLICKHOUSE_CLOUD_KEY_SECRET=dev-key-secret
CLICKHOUSE_CLOUD_READONLY=false
```
</details>

<details>
<summary><strong>Analysis Only Mode</strong></summary>

```env
# Database - read-only for data analysis
CLICKHOUSE_HOST=analytics.company.com
CLICKHOUSE_USER=analyst
CLICKHOUSE_PASSWORD=analyst-password
CLICKHOUSE_SECURE=true
CLICKHOUSE_READONLY=true

# Cloud - monitoring only, no infrastructure changes
CLICKHOUSE_CLOUD_KEY_ID=monitoring-key-id
CLICKHOUSE_CLOUD_KEY_SECRET=monitoring-key-secret
CLICKHOUSE_CLOUD_READONLY=true
```
</details>

### Example Configurations

<details>
<summary><strong>Local Development with Docker</strong></summary>

```env
# Database only - full access for development
CLICKHOUSE_HOST=localhost
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=clickhouse
CLICKHOUSE_SECURE=false
CLICKHOUSE_PORT=8123
CLICKHOUSE_READONLY=false
```
</details>

<details>
<summary><strong>ClickHouse Cloud (Safe Mode)</strong></summary>

```env
# Database connection - read-only
CLICKHOUSE_HOST=your-instance.clickhouse.cloud
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your-database-password
CLICKHOUSE_SECURE=true
CLICKHOUSE_READONLY=true

# Cloud management - monitoring only (explicitly set to true)
CLICKHOUSE_CLOUD_KEY_ID=your-cloud-key-id
CLICKHOUSE_CLOUD_KEY_SECRET=your-cloud-key-secret
CLICKHOUSE_CLOUD_READONLY=true
```
</details>

<details>
<summary><strong>SSL Issues Troubleshooting</strong></summary>

If you encounter SSL certificate verification issues:

```env
# Disable SSL verification for database
CLICKHOUSE_VERIFY=false
CLICKHOUSE_SECURE=false  # Use HTTP instead of HTTPS
CLICKHOUSE_PORT=8123     # HTTP port instead of 8443

# Disable SSL verification for cloud API
CLICKHOUSE_CLOUD_SSL_VERIFY=false
```
</details>

## 🛠️ Available Tools

### 📊 Database Tools (3 tools)

These tools work with any ClickHouse database when database configuration is provided:

- **`list_databases()`** - List all available databases
- **`list_tables(database, like?, not_like?)`** - List tables with detailed metadata including schema, row counts, and column information
- **`run_query(query)`** - Execute queries with safety controls:
  - **Read-only mode** (`CLICKHOUSE_READONLY=true`): Only SELECT, SHOW, DESCRIBE, EXPLAIN queries
  - **Full access mode** (`CLICKHOUSE_READONLY=false`): All SQL operations including INSERT, UPDATE, DELETE, CREATE, DROP

> [!NOTE]
> **Query Safety:** When `CLICKHOUSE_READONLY=true`, all queries automatically run with `readonly = 1` setting and are filtered to prevent data modification operations.

### ☁️ Cloud Management Tools (50+ tools)

These tools work with ClickHouse Cloud when API credentials are provided. Tool availability depends on the `CLICKHOUSE_CLOUD_READONLY` setting:

#### 🔍 Read-Only Operations (Available when `CLICKHOUSE_CLOUD_READONLY=true`)
**Organization Monitoring (3 tools)**
- `cloud_list_organizations()` - List available organizations
- `cloud_get_organization(organization_id)` - Get organization details
- `cloud_get_organization_metrics(organization_id, filtered_metrics?)` - Get Prometheus metrics

**Service Monitoring (3 tools)**
- `cloud_list_services(organization_id)` - List all services in organization
- `cloud_get_service(organization_id, service_id)` - Get detailed service information
- `cloud_get_service_metrics(organization_id, service_id, filtered_metrics?)` - Get service performance metrics

**Resource Inspection (8 tools)**
- `cloud_list_api_keys(organization_id)` - List all API keys (metadata only)
- `cloud_get_api_key(organization_id, key_id)` - Get API key details
- `cloud_list_members(organization_id)` - List organization members
- `cloud_get_member(organization_id, user_id)` - Get member details
- `cloud_list_invitations(organization_id)` - List pending invitations
- `cloud_get_invitation(organization_id, invitation_id)` - Get invitation details
- `cloud_list_backups(organization_id, service_id)` - List service backups
- `cloud_get_backup(organization_id, service_id, backup_id)` - Get backup details

**Configuration Inspection (5 tools)**
- `cloud_get_backup_configuration(organization_id, service_id)` - Get backup configuration
- `cloud_get_private_endpoint_config(organization_id, service_id)` - Get private endpoint configuration
- `cloud_list_clickpipes(organization_id, service_id)` - List ClickPipes
- `cloud_get_clickpipe(organization_id, service_id, clickpipe_id)` - Get ClickPipe details
- `cloud_get_available_regions()` - Get supported regions

**Analytics & Monitoring (3 tools)**
- `cloud_list_activities(organization_id, from_date?, to_date?)` - Get audit logs
- `cloud_get_activity(organization_id, activity_id)` - Get activity details
- `cloud_get_usage_cost(organization_id, from_date, to_date)` - Get usage analytics

#### ⚠️ Write Operations (Available only when `CLICKHOUSE_CLOUD_READONLY=false`)
**Organization Management (2 tools)**
- `cloud_update_organization(organization_id, name?, private_endpoints?)` - Update organization settings
- `cloud_get_organization_private_endpoint_info(organization_id, cloud_provider, region)` - Get private endpoint info

**Service Management (9 tools)**
- `cloud_create_service(organization_id, name, provider, region, ...)` - Create new service
- `cloud_update_service(organization_id, service_id, ...)` - Update service settings
- `cloud_update_service_state(organization_id, service_id, command)` - Start/stop services
- `cloud_update_service_scaling(organization_id, service_id, ...)` - Configure scaling (legacy)
- `cloud_update_service_replica_scaling(organization_id, service_id, ...)` - Configure replica scaling
- `cloud_update_service_password(organization_id, service_id, ...)` - Update service password
- `cloud_create_service_private_endpoint(organization_id, service_id, id, description)` - Create private endpoint
- `cloud_delete_service(organization_id, service_id)` - Delete service

**API Key Management (3 tools)**
- `cloud_create_api_key(organization_id, name, roles, ...)` - Create new API key
- `cloud_update_api_key(organization_id, key_id, ...)` - Update API key properties
- `cloud_delete_api_key(organization_id, key_id)` - Delete API key

**User Management (3 tools)**
- `cloud_update_member_role(organization_id, user_id, role)` - Update member role
- `cloud_remove_member(organization_id, user_id)` - Remove member
- `cloud_create_invitation(organization_id, email, role)` - Send invitation
- `cloud_delete_invitation(organization_id, invitation_id)` - Cancel invitation

**Infrastructure Management (12 tools)**
- `cloud_update_backup_configuration(organization_id, service_id, ...)` - Update backup settings
- `cloud_create_clickpipe(organization_id, service_id, name, description, source, destination, field_mappings?)` - Create ClickPipe
- `cloud_update_clickpipe(organization_id, service_id, clickpipe_id, ...)` - Update ClickPipe
- `cloud_update_clickpipe_scaling(organization_id, service_id, clickpipe_id, replicas?)` - Scale ClickPipe
- `cloud_update_clickpipe_state(organization_id, service_id, clickpipe_id, command)` - Control ClickPipe state
- `cloud_delete_clickpipe(organization_id, service_id, clickpipe_id)` - Delete ClickPipe
- `cloud_list_reverse_private_endpoints(organization_id, service_id)` - List reverse private endpoints
- `cloud_create_reverse_private_endpoint(organization_id, service_id, ...)` - Create reverse private endpoint
- `cloud_get_reverse_private_endpoint(organization_id, service_id, reverse_private_endpoint_id)` - Get details
- `cloud_delete_reverse_private_endpoint(organization_id, service_id, reverse_private_endpoint_id)` - Delete endpoint
- `cloud_create_query_endpoint_config(organization_id, service_id, roles, open_api_keys, allowed_origins)` - Create query config
- `cloud_delete_query_endpoint_config(organization_id, service_id)` - Delete query config

> [!CAUTION]
> **Production Warning:** Write operations can create billable resources, modify running services, or delete infrastructure. Always use `CLICKHOUSE_CLOUD_READONLY=true` in production unless infrastructure changes are specifically required.

## 💡 Usage Examples

### 📊 Database Operations Examples

#### Safe Analysis Mode
```python
# With CLICKHOUSE_READONLY=true (recommended for production)
# Only analytical queries are allowed

# Explore database structure
databases = list_databases()
print(f"Available databases: {[db['name'] for db in databases]}")

# Get detailed table information
tables = list_tables("my_database")
for table in tables:
    print(f"Table: {table['name']}, Rows: {table['total_rows']}")

# Execute analytical queries safely
result = run_query("""
    SELECT 
        date_trunc('day', timestamp) as day,
        count(*) as events,
        avg(value) as avg_value
    FROM my_table 
    WHERE timestamp >= '2024-01-01'
    GROUP BY day
    ORDER BY day
""")

# These queries would be blocked in readonly mode:
# run_query("DROP TABLE my_table")  # ❌ Blocked
# run_query("INSERT INTO my_table VALUES (1)")  # ❌ Blocked
# run_query("UPDATE my_table SET value = 0")  # ❌ Blocked
```

#### Full Access Mode
```python
# With CLICKHOUSE_READONLY=false (development only)
# All SQL operations are allowed

# Data modification operations
run_query("""
    CREATE TABLE test_table (
        id UInt32,
        name String,
        created_at DateTime
    ) ENGINE = MergeTree()
    ORDER BY id
""")

run_query("INSERT INTO test_table VALUES (1, 'test', now())")
run_query("UPDATE test_table SET name = 'updated' WHERE id = 1")
```

### ☁️ Cloud Management Examples

#### Monitoring Mode (Safe)
```python
# With CLICKHOUSE_CLOUD_READONLY=true (recommended for production)
# Only monitoring and inspection operations

# Monitor organization resources
orgs = cloud_list_organizations()
for org in orgs:
    services = cloud_list_services(org['id'])
    print(f"Organization: {org['name']}, Services: {len(services)}")
    
    # Get service metrics
    for service in services:
        metrics = cloud_get_service_metrics(org['id'], service['id'])
        print(f"Service {service['name']} metrics: {metrics}")

# Monitor costs and usage
usage = cloud_get_usage_cost(
    organization_id="org-123",
    from_date="2024-01-01",
    to_date="2024-01-31"
)
print(f"Monthly cost: ${usage['total_cost']}")

# Audit recent activities
activities = cloud_list_activities(
    organization_id="org-123",
    from_date="2024-01-01T00:00:00Z"
)
print(f"Recent activities: {len(activities)} events")

# These operations would be blocked in readonly mode:
# cloud_create_service(...)  # ❌ Blocked
# cloud_delete_service(...)  # ❌ Blocked  
# cloud_update_service_state(...)  # ❌ Blocked
```

#### Infrastructure Management (Full Access)
```python
# With CLICKHOUSE_CLOUD_READONLY=false (use with caution)
# All infrastructure operations allowed

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

### 🔄 Safe Combined Workflow Example

```python
# Production-safe configuration for monitoring and analysis
# CLICKHOUSE_READONLY=true + CLICKHOUSE_CLOUD_READONLY=true

# 1. Monitor existing cloud infrastructure
orgs = cloud_list_organizations()
org_id = orgs[0]['id']

services = cloud_list_services(org_id)
active_services = [s for s in services if s['state'] == 'running']
print(f"Active services: {len(active_services)}")

# 2. Analyze data from running services
for service in active_services:
    # Check service health
    metrics = cloud_get_service_metrics(org_id, service['id'])
    
    # Analyze data (read-only queries)
    if service['endpoints']:
        # Connect to database (would use service endpoint)
        result = run_query("""
            SELECT 
                database,
                table,
                sum(rows) as total_rows,
                sum(bytes_on_disk) as disk_usage
            FROM system.parts
            WHERE active = 1
            GROUP BY database, table
            ORDER BY total_rows DESC
            LIMIT 10
        """)
        
        print(f"Top tables in {service['name']}: {result}")

# 3. Generate usage report
usage = cloud_get_usage_cost(
    organization_id=org_id,
    from_date="2024-01-01",
    to_date="2024-01-31"
)

activities = cloud_list_activities(org_id)
recent_changes = [a for a in activities if 'create' in a.get('action', '').lower()]

print(f"""
Monthly Report:
- Total Cost: ${usage.get('total_cost', 'N/A')}
- Active Services: {len(active_services)}
- Recent Infrastructure Changes: {len(recent_changes)}
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
   # Database configuration (development mode)
   CLICKHOUSE_HOST=localhost
   CLICKHOUSE_PORT=8123
   CLICKHOUSE_USER=default
   CLICKHOUSE_PASSWORD=clickhouse
   CLICKHOUSE_SECURE=false
   CLICKHOUSE_READONLY=false
   
   # Cloud configuration (optional, safe mode)
   CLICKHOUSE_CLOUD_KEY_ID=your-key-id
   CLICKHOUSE_CLOUD_KEY_SECRET=your-key-secret
   CLICKHOUSE_CLOUD_READONLY=true
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

### Testing Safety Features

```bash
# Test read-only database mode
CLICKHOUSE_READONLY=true python -m chmcp.main

# Test cloud monitoring mode  
CLICKHOUSE_CLOUD_READONLY=true python -m chmcp.main

# Test full access mode (development only)
CLICKHOUSE_READONLY=false CLICKHOUSE_CLOUD_READONLY=false python -m chmcp.main
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

**Problem:** Queries are being blocked
- ✅ Check if `CLICKHOUSE_READONLY=true` is preventing write operations
- ✅ For development, temporarily set `CLICKHOUSE_READONLY=false`
- ✅ Review query for prohibited operations (INSERT, UPDATE, DELETE, CREATE, DROP)
- ✅ Use SHOW, DESCRIBE, EXPLAIN, or SELECT queries instead

### ☁️ Cloud API Issues

**Problem:** Cloud tools not working
- ✅ Verify `CLICKHOUSE_CLOUD_KEY_ID` and `CLICKHOUSE_CLOUD_KEY_SECRET` are correct
- ✅ Check API key permissions in ClickHouse Cloud Console
- ✅ Ensure API key is active and not expired
- ✅ For SSL issues, try setting `CLICKHOUSE_CLOUD_SSL_VERIFY=false`

**Problem:** "Operation not permitted" errors
- ✅ Check if `CLICKHOUSE_CLOUD_READONLY=true` is blocking write operations
- ✅ For infrastructure management, set `CLICKHOUSE_CLOUD_READONLY=false`
- ✅ Verify API key has sufficient permissions for the requested operation
- ✅ Review operation type: monitoring operations work in readonly mode, management operations require write access

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

**Problem:** Safety features not working as expected
- ✅ Confirm environment variables are properly set: `echo $CLICKHOUSE_READONLY`
- ✅ Check boolean values are strings: `"true"` not `true` in JSON config
- ✅ Restart the MCP server after changing readonly settings
- ✅ Test with simple operations first to verify behavior

**Problem:** Import errors or missing dependencies
```bash
# Reinstall with latest dependencies
uv sync --force
# Or manual installation
pip install -r requirements.txt --force-reinstall
```

### 🔒 Safety Configuration Troubleshooting

**Problem:** Want to enable write operations temporarily
```bash
# For database operations
export CLICKHOUSE_READONLY=false
# For cloud operations  
export CLICKHOUSE_CLOUD_READONLY=false
# Restart MCP server
```

**Problem:** Accidentally enabled write mode in production
```bash
# Immediately disable write operations
export CLICKHOUSE_READONLY=true
export CLICKHOUSE_CLOUD_READONLY=true
# Restart MCP server
# Review audit logs: cloud_list_activities()
```

**Problem:** Unclear which operations are blocked
- ✅ **Database readonly mode blocks:** INSERT, UPDATE, DELETE, CREATE, DROP, ALTER, TRUNCATE
- ✅ **Database readonly mode allows:** SELECT, SHOW, DESCRIBE, EXPLAIN, WITH (read-only)
- ✅ **Cloud readonly mode blocks:** create_*, update_*, delete_*, start/stop services
- ✅ **Cloud readonly mode allows:** list_*, get_*, metrics, monitoring, analytics

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

**Developed by [Badr Ouali](https://github.com/oualib)**