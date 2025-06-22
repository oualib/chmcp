# MCP ClickHouse Cloud Server

[![PyPI - Version](https://img.shields.io/pypi/v/mcp-clickhouse-cloud)](https://pypi.org/project/mcp-clickhouse-cloud)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A comprehensive Model Context Protocol (MCP) server for ClickHouse database operations and ClickHouse Cloud management.

## 🚀 Quick Start

Start with our step-by-step tutorial:

👉 **[Complete Setup Tutorial](tutorial/README.md)** - Transform Claude into a powerful ClickHouse data agent

For experienced users, jump to the [Quick Configuration](#quick-configuration) section below.

## 📚 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [📚 Table of Contents](#-table-of-contents)
- [🌟 Why This Server?](#-why-this-server)
- [✨ Features](#-features)
  - [Database Operations](#database-operations)
  - [ClickHouse Cloud Management (50+ Tools)](#clickhouse-cloud-management-50-tools)
- [⚡ Quick Configuration](#-quick-configuration)
  - [Claude Desktop Setup](#claude-desktop-setup)
  - [For ClickHouse Cloud](#for-clickhouse-cloud)
  - [For Your Own ClickHouse Server](#for-your-own-clickhouse-server)
  - [For ClickHouse SQL Playground (Free Testing)](#for-clickhouse-sql-playground-free-testing)
- [📦 Installation](#-installation)
  - [Option 1: Using uv (Recommended)](#option-1-using-uv-recommended)
  - [Option 2: Manual Installation](#option-2-manual-installation)
- [⚙️ Environment Variables](#️-environment-variables)
  - [Database Configuration (Required for database tools)](#database-configuration-required-for-database-tools)
  - [Cloud API Configuration (Required for cloud tools)](#cloud-api-configuration-required-for-cloud-tools)
  - [Example Configurations](#example-configurations)
- [🛠️ Available Tools](#️-available-tools)
  - [Database Tools (3 tools)](#database-tools-3-tools)
  - [Cloud Tools (50+ tools)](#cloud-tools-50-tools)
- [💡 Examples](#-examples)
  - [Query Database](#query-database)
  - [Manage Cloud Services](#manage-cloud-services)
- [🔧 Development](#-development)
  - [Local Development Setup](#local-development-setup)
  - [Running Tests](#running-tests)
- [📁 Project Structure](#-project-structure)
- [🔍 How MCP Tool Discovery Works](#-how-mcp-tool-discovery-works)
- [🔑 Getting ClickHouse Cloud API Keys](#-getting-clickhouse-cloud-api-keys)
- [🐛 Troubleshooting](#-troubleshooting)
  - [Database Connection Issues](#database-connection-issues)
  - [Cloud API Issues](#cloud-api-issues)
  - [Missing Tools](#missing-tools)
- [📄 License](#-license)

## Why This Server?

This repository is a significant improvement over the [original ClickHouse MCP server](https://github.com/ClickHouse/mcp-clickhouse). While the original server only supports basic database operations (list databases, run SELECT queries, and list tables), this enhanced version provides:

- **50+ Cloud Management Tools**: Complete ClickHouse Cloud API integration for organizations, services, API keys, members, backups, and more
- **Superior Code Quality**: Well-structured, maintainable codebase with proper error handling and type hints
- **Enhanced Database Operations**: Extended functionality with metadata access and safety guarantees
- **Production Ready**: Comprehensive configuration options, SSL support, and robust error handling

Feature | Original Server | This Server
-- | -- | --
Database Operations | 3 basic tools | 3 enhanced tools with safety
Cloud Management | ❌ None | ✅ 50+ comprehensive tools
Code Quality | Basic | Production-ready with proper structure
SSL Support | Limited | Full SSL configuration options
Error Handling | Basic | Robust with detailed error messages

## Features

### Database Operations
- **List databases**: Get all available databases
- **List tables**: Get detailed table information including schema, row counts, and column details
- **Run SELECT queries**: Execute read-only queries with timeout protection and safety guarantees
- **Metadata access**: Full access to ClickHouse system tables

### ClickHouse Cloud Management (50+ Tools)
- **Organizations**: List, get details, update settings, view metrics
- **Services**: Create, manage, start/stop, configure scaling, delete services
- **API Keys**: Create, list, update, delete API keys
- **Members**: Manage organization members and roles  
- **Invitations**: Send and manage organization invitations
- **Backups**: List, configure, and manage service backups
- **ClickPipes**: Manage data ingestion pipelines (Beta)
- **Activities**: View audit logs and organization activities
- **Usage & Costs**: Get detailed usage and cost analytics
- **Private Endpoints**: Configure private network access

## Configuration

### Claude Desktop Setup

1. Open the Claude Desktop configuration file located at:
   * On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   * On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following configuration:

#### For Your Own ClickHouse Server
```json
{
  "mcpServers": {
    "mcp-clickhouse-cloud": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp-clickhouse-cloud",
        "--python",
        "3.13",
        "mcp-clickhouse-cloud"
      ],
      "env": {
        "CLICKHOUSE_HOST": "",
        "CLICKHOUSE_PORT": "",
        "CLICKHOUSE_USER": "",
        "CLICKHOUSE_PASSWORD": "",
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_VERIFY": "true",
        "CLICKHOUSE_CONNECT_TIMEOUT": "30",
        "CLICKHOUSE_SEND_RECEIVE_TIMEOUT": "300"
      }
    }
  }
}
```

#### For ClickHouse SQL Playground (Free Testing)
```json
{
  "mcpServers": {
    "mcp-clickhouse-cloud": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp-clickhouse-cloud",
        "--python",
        "3.13",
        "mcp-clickhouse-cloud"
      ],
      "env": {
        "CLICKHOUSE_HOST": "sql-clickhouse.clickhouse.com",
        "CLICKHOUSE_PORT": "8443",
        "CLICKHOUSE_USER": "demo",
        "CLICKHOUSE_PASSWORD": "",
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_VERIFY": "true",
        "CLICKHOUSE_CONNECT_TIMEOUT": "30",
        "CLICKHOUSE_SEND_RECEIVE_TIMEOUT": "300"
      }
    }
  }
}
```

3. **Important**: Locate the command entry for `uv` and replace it with the absolute path to the `uv` executable. On macOS, find this path using `which uv`.

4. Restart Claude Desktop to apply the changes.

## Installation

### Option 1: Using uv (Recommended)
```bash
# Install via uv (used by Claude Desktop)
uv add mcp-clickhouse-cloud
```

### Option 2: Manual Installation
```bash
# Clone the repository
git clone 
cd mcp-clickhouse-cloud

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

## Environment Variables

### Database Configuration (Required for database tools)

#### Required Variables
```bash
CLICKHOUSE_HOST=your-clickhouse-host.com    # ClickHouse server hostname
CLICKHOUSE_USER=your-username               # Username for authentication
CLICKHOUSE_PASSWORD=your-password           # Password for authentication
```

> [!CAUTION]
> Treat your MCP database user as you would any external client connecting to your database. Grant only the minimum necessary privileges required for operation. Avoid using default or administrative users.

#### Optional Variables (with defaults)
```bash
CLICKHOUSE_PORT=8443                        # 8443 for secure, 8123 for non-secure
CLICKHOUSE_SECURE=true                      # Enable HTTPS connection
CLICKHOUSE_VERIFY=true                      # Verify SSL certificates
CLICKHOUSE_CONNECT_TIMEOUT=30               # Connection timeout in seconds
CLICKHOUSE_SEND_RECEIVE_TIMEOUT=300         # Query timeout in seconds
CLICKHOUSE_DATABASE=default                 # Default database to use
CLICKHOUSE_PROXY_PATH=                      # Path for HTTP proxy
```

#### SSL Configuration Issues
If you encounter SSL certificate verification issues, you can disable SSL verification:
```bash
CLICKHOUSE_VERIFY=false                     # Disable SSL certificate verification
```

### Cloud API Configuration (Required for cloud tools)
```bash
# Required - Get these from ClickHouse Cloud Console
CLICKHOUSE_CLOUD_KEY_ID=your-cloud-key-id
CLICKHOUSE_CLOUD_KEY_SECRET=your-cloud-key-secret

# Optional
CLICKHOUSE_CLOUD_API_URL=https://api.clickhouse.cloud
CLICKHOUSE_CLOUD_TIMEOUT=30
CLICKHOUSE_CLOUD_SSL_VERIFY=true           # Set to "false" for SSL issues
```

#### Cloud API SSL Configuration Issues
If you encounter SSL certificate verification issues with the Cloud API:
```bash
CLICKHOUSE_CLOUD_SSL_VERIFY=false          # Disable SSL certificate verification for Cloud API
```

### Example Configurations

#### Local Development with Docker
```env
CLICKHOUSE_HOST=localhost
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=clickhouse
CLICKHOUSE_SECURE=false                     # Uses port 8123 automatically
CLICKHOUSE_VERIFY=false
```

#### ClickHouse Cloud
```env
CLICKHOUSE_HOST=your-instance.clickhouse.cloud
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=your-password
# CLICKHOUSE_SECURE=true                    # Uses port 8443 automatically
# CLICKHOUSE_DATABASE=your_database
```

#### ClickHouse SQL Playground
```env
CLICKHOUSE_HOST=sql-clickhouse.clickhouse.com
CLICKHOUSE_USER=demo
CLICKHOUSE_PASSWORD=
# Uses secure defaults (HTTPS on port 8443)
```

## Available Tools

### Database Tools (3 tools)
- `list_databases()` - List all databases
- `list_tables(database, like?, not_like?)` - List tables with metadata  
- `run_select_query(query)` - Execute SELECT queries (all queries run with `readonly = 1` for safety)

### Cloud Tools (50+ tools)

#### Organization Management
- `cloud_list_organizations()` - List available organizations
- `cloud_get_organization(organization_id)` - Get organization details
- `cloud_update_organization(organization_id, name?)` - Update organization
- `cloud_get_organization_metrics(organization_id, filtered_metrics?)` - Get Prometheus metrics

#### Service Management
- `cloud_list_services(organization_id)` - List all services
- `cloud_get_service(organization_id, service_id)` - Get service details
- `cloud_create_service(organization_id, name, provider, region, ...)` - Create new service
- `cloud_update_service_state(organization_id, service_id, command)` - Start/stop service
- `cloud_update_service_scaling(organization_id, service_id, ...)` - Configure auto-scaling
- `cloud_update_service_password(organization_id, service_id, ...)` - Update password
- `cloud_delete_service(organization_id, service_id)` - Delete service
- `cloud_get_service_metrics(organization_id, service_id, ...)` - Get service metrics

#### API Key Management
- `cloud_list_api_keys(organization_id)` - List API keys
- `cloud_create_api_key(organization_id, name, roles, ...)` - Create API key
- `cloud_delete_api_key(organization_id, key_id)` - Delete API key

#### Member Management  
- `cloud_list_members(organization_id)` - List organization members
- `cloud_update_member_role(organization_id, user_id, role)` - Update member role
- `cloud_remove_member(organization_id, user_id)` - Remove member

#### Invitation Management
- `cloud_list_invitations(organization_id)` - List pending invitations
- `cloud_create_invitation(organization_id, email, role)` - Send invitation
- `cloud_delete_invitation(organization_id, invitation_id)` - Cancel invitation

#### Backup Management
- `cloud_list_backups(organization_id, service_id)` - List service backups
- `cloud_get_backup(organization_id, service_id, backup_id)` - Get backup details
- `cloud_get_backup_configuration(organization_id, service_id)` - Get backup config
- `cloud_update_backup_configuration(organization_id, service_id, ...)` - Update backup settings

#### ClickPipes Management (Beta)
- `cloud_list_clickpipes(organization_id, service_id)` - List ClickPipes
- `cloud_get_clickpipe(organization_id, service_id, clickpipe_id)` - Get ClickPipe details
- `cloud_update_clickpipe_state(organization_id, service_id, clickpipe_id, command)` - Start/stop ClickPipe
- `cloud_delete_clickpipe(organization_id, service_id, clickpipe_id)` - Delete ClickPipe

#### Activity & Audit Logs
- `cloud_list_activities(organization_id, from_date?, to_date?)` - Get activity logs
- `cloud_get_activity(organization_id, activity_id)` - Get activity details

#### Usage & Cost Analytics
- `cloud_get_usage_cost(organization_id, from_date, to_date)` - Get cost breakdown

#### Utilities
- `cloud_get_available_regions()` - Get supported cloud regions and providers
- `cloud_get_private_endpoint_config(organization_id, service_id)` - Get private endpoint config

## Development

### Local Development Setup

1. **Start ClickHouse cluster**:
   ```bash
   cd test-services
   docker compose up -d
   ```

2. **Create environment file**:
   ```bash
   # Create .env file in repository root
   cat > .env << EOF
   CLICKHOUSE_HOST=localhost
   CLICKHOUSE_PORT=8123
   CLICKHOUSE_USER=default
   CLICKHOUSE_PASSWORD=clickhouse
   CLICKHOUSE_SECURE=false
   EOF
   ```

3. **Install dependencies**:
   ```bash
   uv sync                               # Install dependencies
   source .venv/bin/activate            # Activate virtual environment
   ```

4. **Run the MCP server**:
   ```bash
   mcp dev mcp_clickhouse_cloud/mcp_server.py  # Start for testing
   # OR
   python -m mcp_clickhouse_cloud.main         # Start normally
   ```

### Running Tests

```bash
uv sync --all-extras --dev              # Install dev dependencies
uv run ruff check .                     # Run linting

docker compose up -d test_services      # Start ClickHouse
uv run pytest tests                     # Run tests
```

## Project Structure

```
mcp_clickhouse_cloud/
├── __init__.py                 # Package initialization
├── main.py                     # Entry point
├── mcp_env.py                  # Database environment configuration
├── mcp_server.py              # Main server + database tools
├── cloud_config.py            # Cloud API configuration
├── cloud_client.py            # HTTP client for Cloud API
└── cloud_tools.py             # Cloud MCP tools (50+ tools)
```

## How MCP Tool Discovery Works

1. **Decorator Registration**: All tools use the `@mcp.tool()` decorator
2. **Import-based Discovery**: When modules are imported, FastMCP automatically scans for decorated functions
3. **Automatic Registration**: All discovered tools become available through the MCP protocol
4. **No Manual Setup**: No need to manually register tools or maintain tool lists

## Getting ClickHouse Cloud API Keys

1. Log into [ClickHouse Cloud Console](https://console.clickhouse.cloud/)
2. Go to **Settings** → **API Keys**
3. Click **Create API Key**
4. Choose appropriate permissions (admin, developer, etc.)
5. Copy the Key ID and Key Secret to your `.env` file

## Examples

### Query Database
```python
# List all databases
databases = list_databases()

# List tables in a specific database  
tables = list_tables("my_database")

# Run a SELECT query
result = run_select_query("SELECT count() FROM my_table")
```

### Manage Cloud Services
```python
# List organizations
orgs = cloud_list_organizations()

# Create a new service
service = cloud_create_service(
    organization_id="org-123",
    name="my-service", 
    provider="aws",
    region="us-east-1"
)

# Start the service
cloud_update_service_state(
    organization_id="org-123",
    service_id="service-456", 
    command="start"
)
```

## Troubleshooting

### Database Connection Issues
- Verify `CLICKHOUSE_HOST`, `CLICKHOUSE_USER`, and `CLICKHOUSE_PASSWORD`
- Check network connectivity to ClickHouse server
- Ensure firewall allows connections on the specified port
- For SSL issues, try setting `CLICKHOUSE_VERIFY=false`

### Cloud API Issues  
- Verify `CLICKHOUSE_CLOUD_KEY_ID` and `CLICKHOUSE_CLOUD_KEY_SECRET`
- Check API key permissions in ClickHouse Cloud Console
- Ensure API key is not expired or disabled
- For SSL issues, try setting `CLICKHOUSE_CLOUD_SSL_VERIFY=false`

### Missing Tools
- Database tools require database configuration
- Cloud tools require cloud API configuration
- Check logs for import errors or missing dependencies

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

Developed by Badr Ouali.
