# Step-by-Step Tutorial: Setting Up Claude as a ClickHouse Data Agent

Transform Claude into a powerful data agent that can query your ClickHouse databases, manage cloud services, and create interactive dashboards. This tutorial covers both ClickHouse Cloud and on-premises setups.

## 📚 Table of Contents

- [🎯 What You'll Achieve](#-what-youll-achieve)
- [📋 Prerequisites](#-prerequisites)
- [🚀 Part 1: Setting Up ClickHouse Cloud (Recommended)](#-part-1-setting-up-clickhouse-cloud-recommended)
  - [Step 1: Create Your ClickHouse Cloud Account](#step-1-create-your-clickhouse-cloud-account)
  - [Step 2: Create Your First Service](#step-2-create-your-first-service)
  - [Step 3: Create an API Key for Claude](#step-3-create-an-api-key-for-claude)
  - [Step 4: Create a Query Endpoint](#step-4-create-a-query-endpoint)
- [💻 Part 2: Installing Claude Desktop](#-part-2-installing-claude-desktop)
  - [Step 1: Download Claude Desktop](#step-1-download-claude-desktop)
  - [Step 2: Choose Your Plan](#step-2-choose-your-plan)
- [🔧 Part 3: Installing UV Package Manager](#-part-3-installing-uv-package-manager)
  - [Step 1: Install UV](#step-1-install-uv)
  - [Step 2: Locate UV Path](#step-2-locate-uv-path)
- [⚙️ Part 4: Configuring Claude for ClickHouse](#️-part-4-configuring-claude-for-clickhouse)
  - [Step 1: Access Claude Configuration](#step-1-access-claude-configuration)
  - [Step 2: Configure for ClickHouse Cloud](#step-2-configure-for-clickhouse-cloud)
  - [Step 3: Configure for On-Premises ClickHouse](#step-3-configure-for-on-premises-clickhouse)
  - [Step 4: Update with UV Path](#step-4-update-with-uv-path)
  - [Step 5: Save and Restart](#step-5-save-and-restart)
- [🎉 Part 5: Testing Your Setup](#-part-5-testing-your-setup)
  - [Step 1: Verify Connection](#step-1-verify-connection)
  - [Step 2: Explore Your Data](#step-2-explore-your-data)
  - [Step 3: Test Cloud Management](#step-3-test-cloud-management-cloud-users-only)
- [🚀 Part 6: What You Can Do Now](#-part-6-what-you-can-do-now)
  - [📊 Data Analysis and Visualization](#-data-analysis-and-visualization)
  - [🎨 Interactive Dashboards](#-interactive-dashboards)
  - [☁️ Cloud Management](#️-cloud-management-cloud-users)
  - [🔧 Database Administration](#-database-administration)
- [🔧 Troubleshooting](#-troubleshooting)
- [🎯 Next Steps](#-next-steps)
- [🏆 Conclusion](#-conclusion)

## 🎯 What You'll Achieve

By the end of this tutorial, you'll have Claude configured to:
- Query your ClickHouse databases with natural language
- Manage ClickHouse Cloud services and resources
- Analyze data and create visualizations
- Monitor usage, costs, and performance metrics
- Manage API keys, members, and organizational settings

## 📋 Prerequisites

- A computer with internet access
- Basic familiarity with JSON configuration files
- A ClickHouse database (Cloud or on-premises)

## 🚀 Part 1: Setting Up ClickHouse Cloud (Recommended)

### Step 1: Create Your ClickHouse Cloud Account

1. **Visit ClickHouse Cloud**
   - Go to [https://clickhouse.com/cloud](https://clickhouse.com/cloud)

   ![ClickHouse Cloud Homepage](images/01-clickhouse-homepage.png)

2. **Sign Up for Free Account**
   - Enter your email and create a password
   - Verify your email address
   - **🎉 You'll receive $300 in free ClickHouse credits!**

   ![Sign Up Form](images/02-signup-form.png)

### Step 2: Create Your First Service

1. **Access the Console**
   - After verification, you'll be redirected to the ClickHouse Cloud Console
   - Click **"New Service"**

   ![Cloud Console Dashboard](images/03-console-dashboard.png)

2. **Configure Your Service**
   - **Name**: Give your service a meaningful name (e.g., "my-data-analytics")
   - **Cloud Provider**: Choose **AWS** (for this tutorial)
   - **Region**: Select **us-east-1** or the region closest to you for better performance
   - **Tier**: Start with "Development" for testing (you can upgrade later)

   --- ![Service Configuration](images/04-service-config.png)

3. **Create and Wait**
   - Click **"Create service"**
   - Wait 2-3 minutes for your service to be provisioned
   - ✅ Your service status will change to "Running"

   --- ![Service Creation Progress](images/05-service-creating.png)

### Step 3: Create an API Key for Claude

> **🔐 Why do we need an API key?**
> 
> API keys allow Claude to securely access your ClickHouse Cloud account and perform operations on your behalf. This enables advanced features like:
> - Managing multiple services
> - Monitoring usage and costs
> - Managing team members and permissions
> - Accessing detailed analytics and metrics

1. **Navigate to API Keys**
   - In the left sidebar, click **"Settings"**
   - Click **"API Keys"**
   - Click **"Create API Key"**

   ![API Keys Section](images/06-api-keys-menu.png)

2. **Configure Your API Key**
   - **Name**: Enter a descriptive name like "Claude Agent Key"
   - **Description**: "API key for Claude MCP integration"
   - **Roles**: ⚠️ **Important!** Choose roles carefully for security:
     - **For beginners**: Select "Developer" role (read access + query endpoints)
     - **For advanced users**: Select "Admin" role (full access)
     - **For production**: Create multiple keys with minimal required permissions

   ![API Key Configuration](images/07-api-key-config.png)

3. **Generate and Save Your Credentials**
   - Click **"Create API Key"**
   - **🚨 CRITICAL**: Copy both the **Key ID** and **Key Secret** immediately
   - Store them securely - you won't be able to see the secret again!

   --- ![API Key Generated](images/08-api-key-generated.png)

   ```
   Example credentials (yours will be different):
   Key ID: CHCIAKEXAMPLE123456789
   Key Secret: CHCSexample_secret_key_abc123xyz789
   ```

### Step 4: Create a Query Endpoint

1. **Access Your Service Settings**
   - Go back to **"Services"** in the left sidebar
   - Click on your service name
   - Click **"Settings"** tab

   ![Service Settings](images/09-service-settings.png)

2. **Set Up Query Endpoint**
   - Scroll down to **"Query Endpoints"** section
   - Click **"Add endpoint"**
   - **Endpoint name**: "claude-agent-endpoint"
   - **API Key**: Select the key you just created
   - Click **"Create endpoint"**

   ![Query Endpoint Setup](images/10-query-endpoint.png)

3. **Note Your Connection Details**
   - Click the **"Connect"** button on your service
   - You'll see a popup with all your connection details:
     - **Hostname** (e.g., `abc123.us-east-1.aws.clickhouse.cloud`)
     - **Port** (usually `8443` for secure connections)
     - **Username** (usually `default`)
     - **Password** (auto-generated secure password)
   - Copy these details for use in the configuration

   ![Connection Details](images/11-connection-details.png)

## 🔧 Part 3: Installing UV Package Manager

> **🔑 Why do we need UV?**
> 
> UV is a fast Python package manager that Claude Desktop uses to install and run the MCP ClickHouse Cloud & On-Prem server. It ensures clean, isolated environments and fast package resolution.

### Step 1: Install Python 3.13

**🚨 IMPORTANT**: Install Python 3.13 first, as UV and the MCP server require this version.

1. **Download Python 3.13**
   - Visit [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Download Python 3.13 for your operating system
   - Run the installer and follow the setup wizard

2. **Verify Installation**
   ```bash
   python3.13 --version
   # Should output: Python 3.13.x
   ```

### Step 2: Install UV

1. **Using pip/pip3 (Recommended)**
   ```bash
   # Using pip3
   pip3 install uv
   
   # Or using pip
   pip install uv
   
   # If you have multiple Python versions, be specific:
   python3.13 -m pip install uv
   ```

2. **Alternative Installation Methods**
   - **macOS with Homebrew**: `brew install uv`
   - **Windows with Chocolatey**: `choco install uv`
   - **Using installer script**:
     - **macOS/Linux**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
     - **Windows**: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

### Step 3: Locate UV Path

After installation, you need to find the exact path to the UV executable:

1. **Find UV Path**
   - **macOS/Linux**: Open Terminal and run:
     ```bash
     which uv
     ```
   - **Windows**: Open Command Prompt and run:
     ```cmd
     where uv
     ```

2. **Example Outputs**
   ```bash
   # macOS with Homebrew
   $ which uv
   /opt/homebrew/bin/uv

   # macOS with system Python
   $ which uv
   /Library/Frameworks/Python.framework/Versions/3.13/bin/uv

   # Linux
   $ which uv
   /usr/local/bin/uv

   # Windows
   C:\Users\YourName\.cargo\bin\uv.exe
   ```

3. **Copy the Full Path**
   - Copy the entire path returned by the command
   - You'll need this exact path in the next section
   - ⚠️ **Important**: Using the full path prevents common configuration errors

   ![UV Path Example](images/20-uv-path-example.png)

## ⚙️ Part 4: Configuring Claude for ClickHouse

### Step 1: Download Claude Desktop

1. **Visit Claude Download Page**
   - Go to [https://claude.ai/download](https://claude.ai/download)
   - Choose your operating system (Windows, macOS, or Linux)

   ![Claude Download Page](images/12-claude-download.png)

2. **Install Claude Desktop**
   - Download and run the installer
   - Follow the installation prompts
   - Launch Claude Desktop after installation

### Step 2: Choose Your Plan

1. **Select a Plan**
   - **Free Plan**: Good for basic queries and testing
   - **Pro Plan**: Recommended for serious data work
     - Higher usage limits
     - Access to advanced models
     - Priority support

   ![Claude Plans](images/13-claude-plans.png)

2. **Sign In or Create Account**
   - Use your existing Anthropic account or create a new one
   - Complete the setup process

## 💻 Part 2: Installing Claude Desktop

### Step 1: Access Claude Configuration

1. **Open Configuration File**
   - **On macOS**: Press `Cmd + ,` or go to `Claude → Preferences → Developer`
   - **On Windows**: Press `Ctrl + ,` or go to `File → Settings → Developer`
   - Click **"Edit Config"**

   ![Claude Settings](images/14-claude-settings.png)

2. **Locate Configuration File**
   The configuration file is located at:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

### Step 2: Configure for ClickHouse Cloud

1. **Add MCP Server Configuration**
   Replace the contents of your `claude_desktop_config.json` with:

   ```json
   {
     "mcpServers": {
       "chmcp": {
         "command": "/full/path/to/uv",
         "args": [
           "run",
           "--with",
           "chmcp",
           "--python",
           "3.13",
           "chmcp"
         ],
         "env": {
           "CLICKHOUSE_HOST": "your-service.region.provider.clickhouse.cloud",
           "CLICKHOUSE_PORT": "8443",
           "CLICKHOUSE_USER": "default",
           "CLICKHOUSE_PASSWORD": "your-service-password",
           "CLICKHOUSE_SECURE": "true",
           "CLICKHOUSE_VERIFY": "true",
           "CLICKHOUSE_CLOUD_KEY_ID": "your-api-key-id",
           "CLICKHOUSE_CLOUD_KEY_SECRET": "your-api-key-secret"
         }
       }
     }
   }
   ```

   > **🔧 Troubleshooting SSL Issues?**
   > 
   > If you encounter SSL certificate verification issues, add these settings:
   > ```json
   > "CLICKHOUSE_VERIFY": "false",
   > "CLICKHOUSE_CLOUD_SSL_VERIFY": "false"
   > ```

2. **Update with Your ClickHouse Cloud Credentials**
   Get your connection details by clicking **"Connect"** on your ClickHouse Cloud service:
   
   - `CLICKHOUSE_HOST`: Your service hostname (e.g., `abc123.us-east-1.aws.clickhouse.cloud`)
   - `CLICKHOUSE_PORT`: Usually `8443`
   - `CLICKHOUSE_USER`: Usually `default`
   - `CLICKHOUSE_PASSWORD`: The password shown in the Connect dialog
   - `CLICKHOUSE_CLOUD_KEY_ID`: Your API key ID from Step 3.3
   - `CLICKHOUSE_CLOUD_KEY_SECRET`: Your API key secret from Step 3.3

   ![Configuration Example](images/15-config-example.png)

### Step 3: Configure for On-Premises ClickHouse

If you're using your own ClickHouse server, use this configuration instead:

```json
{
  "mcpServers": {
    "chmcp": {
      "command": "/full/path/to/uv",
      "args": [
        "run",
        "--with",
        "chmcp",
        "--python",
        "3.13",
        "chmcp"
      ],
      "env": {
        "CLICKHOUSE_HOST": "your-clickhouse-server.com",
        "CLICKHOUSE_PORT": "8443",
        "CLICKHOUSE_USER": "your-username",
        "CLICKHOUSE_PASSWORD": "your-password",
        "CLICKHOUSE_SECURE": "true",
        "CLICKHOUSE_VERIFY": "true"
      }
    }
  }
}
```

> **🔧 Troubleshooting SSL Issues?**
> 
> If you encounter SSL certificate verification issues with your on-premises server:
> ```json
> "CLICKHOUSE_VERIFY": "false"
> ```

### Step 4: Update with UV Path

**🚨 CRITICAL STEP**: Replace `/full/path/to/uv` with the actual path you found in Part 3:

1. **Use the UV path from Part 3, Step 2**
   Examples of what your command should look like:
   ```json
   // macOS with Homebrew
   "command": "/opt/homebrew/bin/uv"
   
   // macOS with system Python  
   "command": "/Library/Frameworks/Python.framework/Versions/3.13/bin/uv"
   
   // Linux
   "command": "/usr/local/bin/uv"
   
   // Windows
   "command": "C:\\Users\\YourName\\.cargo\\bin\\uv.exe"
   ```

2. **Complete Configuration Example**
   Here's how your final configuration should look:
   ```json
   {
     "mcpServers": {
       "chmcp": {
         "command": "/Library/Frameworks/Python.framework/Versions/3.13/bin/uv",
         "args": [
           "run",
           "--with", 
           "chmcp",
           "--python",
           "3.13",
           "chmcp"
         ],
         "env": {
           "CLICKHOUSE_HOST": "abc123.us-east-1.aws.clickhouse.cloud",
           "CLICKHOUSE_PORT": "8443",
           "CLICKHOUSE_USER": "default",
           "CLICKHOUSE_PASSWORD": "your-password-here",
           "CLICKHOUSE_SECURE": "true",
           "CLICKHOUSE_VERIFY": "true",
           "CLICKHOUSE_CLOUD_KEY_ID": "CHCIAKEXAMPLE123456789",
           "CLICKHOUSE_CLOUD_KEY_SECRET": "CHCSexample_secret_key_abc123xyz789"
         }
       }
     }
   }
   ```

3. **🔬 For Developers: Testing Local Development**
   If you're developing or testing your own implementation of the MCP server, you can use a local directory path instead:
   
   ```json
   {
     "mcpServers": {
       "chmcp": {
         "command": "/full/path/to/uv",
         "args": [
           "run",
           "--directory",
           "/Users/yourname/path/to/chmcp/chmcp",
           "python",
           "-m",
           "chmcp.main"
         ],
         "env": {
           // ... your environment variables here
         }
       }
     }
   }
   ```
   
   **Replace the directory path with your local repository path:**
   - Clone the repository: `git clone https://github.com/your-repo/chmcp.git`
   - Use the full path to the `chmcp` folder in your clone
   - Example: `/Users/badrouali/Documents/GitHub/chmcp/chmcp`
   
   This is useful for:
   - Testing modifications to the source code
   - Debugging issues during development
   - Contributing to the project
   - Running unreleased features

### Step 5: Save and Restart

1. **Save Configuration**
   - Save the `claude_desktop_config.json` file
   - Make sure the JSON syntax is valid (no trailing commas, proper quotes)

2. **Restart Claude Desktop**
   - Close Claude Desktop completely
   - Reopen the application
   - Wait for the MCP server to initialize (may take 30-60 seconds)

   ![Claude Restart](images/16-claude-restart.png)

## 🎉 Part 5: Testing Your Setup

### Step 1: Verify Connection

1. **Start a New Conversation**
   - Open Claude Desktop
   - Start a new chat
   - Look for the MCP indicator (tool icon) in the interface

2. **Test Basic Database Query**
   ```
   Show me all the databases available in my ClickHouse instance
   ```

   ![First Query](images/17-first-query.png)

### Step 2: Explore Your Data

1. **List Tables**
   ```
   What tables are available in the default database?
   ```

2. **Sample Data Query**
   ```
   Show me the first 10 rows from [your-table-name]
   ```

   ![Data Exploration](images/18-data-exploration.png)

### Step 3: Test Cloud Management (Cloud Users Only)

1. **Check Organization**
   ```
   Show me details about my ClickHouse Cloud organization
   ```

2. **Monitor Usage**
   ```
   What's my current ClickHouse Cloud usage and costs for this month?
   ```

   ![Cloud Management](images/19-cloud-management.png)

## 🚀 Part 6: What You Can Do Now

### 📊 Data Analysis and Visualization

1. **Natural Language Queries**
   ```
   - "What are the top 10 most popular products by sales?"
   - "Show me daily user registrations for the last 30 days"
   - "Create a visualization of revenue trends by month"
   ```

2. **Advanced Analytics**
   ```
   - "Calculate the conversion rate from our marketing campaigns"
   - "Find users who haven't logged in for more than 30 days"
   - "Analyze seasonal patterns in our sales data"
   ```

### 🎨 Interactive Dashboards

Claude can create rich, interactive dashboards:

```
Create an interactive dashboard showing:
1. Total revenue this quarter
2. Top 5 products by sales volume
3. Geographic distribution of customers
4. Monthly growth trends
```

### ☁️ Cloud Management (Cloud Users)

1. **Service Management**
   ```
   - "Show me all my ClickHouse services and their status"
   - "What's the current resource usage of my production service?"
   - "Scale up my analytics service for the upcoming data load"
   ```

2. **Cost Optimization**
   ```
   - "Analyze my ClickHouse Cloud spending for the last 3 months"
   - "Which services are consuming the most resources?"
   - "Show me backup costs and retention policies"
   ```

3. **Team Management**
   ```
   - "List all members in my organization and their roles"
   - "Create an invitation for a new team member with developer access"
   - "Show me recent activity in my organization"
   ```

### 🔧 Database Administration

1. **Performance Monitoring**
   ```
   - "Show me the slowest running queries"
   - "What's the current memory and CPU usage?"
   - "Analyze table sizes and compression ratios"
   ```

2. **Health Checks**
   ```
   - "Check the health of all my database connections"
   - "Show me any recent errors or warnings"
   - "Verify backup status for all services"
   ```

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **"Connection Failed" Error**
   - ✅ Verify your hostname, username, and password
   - ✅ Check that your ClickHouse service is running
   - ✅ Ensure firewall allows connections on the specified port

2. **"API Key Invalid" Error**
   - ✅ Double-check your API key ID and secret
   - ✅ Verify the API key hasn't expired
   - ✅ Ensure the key has the correct permissions

3. **"MCP Server Not Found" Error**
   - ✅ Verify the UV path is correct (use the full path from Part 3)
   - ✅ Restart Claude Desktop
   - ✅ Check the JSON configuration syntax
   - ✅ Try using the absolute path to UV instead of just "uv"

4. **SSL Certificate Issues**
   Add to your configuration:
   ```json
   "CLICKHOUSE_VERIFY": "false",
   "CLICKHOUSE_CLOUD_SSL_VERIFY": "false"
   ```

### Getting Help

- **ClickHouse Cloud Support**: [https://clickhouse.com/support](https://clickhouse.com/support)
- **Claude Support**: [https://support.anthropic.com](https://support.anthropic.com)
- **GitHub Issues**: [Report issues on our repository](https://github.com/your-repo/issues)

## 🎯 Next Steps

1. **Explore Advanced Features**
   - Set up automated reports
   - Create custom dashboards
   - Implement data quality checks

2. **Optimize Performance**
   - Learn about ClickHouse optimization
   - Implement proper indexing strategies
   - Monitor and tune query performance

3. **Scale Your Setup**
   - Add multiple ClickHouse services
   - Implement proper access controls
   - Set up monitoring and alerting

## 🏆 Conclusion

Congratulations! You've successfully transformed Claude into a powerful ClickHouse data agent. You can now:

- ✅ Query your data using natural language
- ✅ Create interactive visualizations and dashboards  
- ✅ Manage your ClickHouse Cloud infrastructure
- ✅ Monitor costs, performance, and team access
- ✅ Perform advanced analytics and reporting

Your data is now just a conversation away! Start exploring and discover insights you never knew existed in your data.

---

**🔗 Useful Links**
- [ClickHouse Documentation](https://clickhouse.com/docs)
- [Claude Desktop Download](https://claude.ai/download)
- [MCP ClickHouse Cloud & On-Prem Repository](https://github.com/your-repo)
- [ClickHouse Cloud Console](https://console.clickhouse.cloud)

**📧 Questions?**
Feel free to open an issue on our GitHub repository or reach out to the community for support!