# Fabric Governance Toolkit

A comprehensive Python-based codebase with Jupyter notebooks for governing Microsoft Fabric. This toolkit provides administrative capabilities for managing workspaces, collecting audit data, managing capacities, and performing migrations.

## Features

- **📊 Audit Data Collection**: Collect and analyze Fabric activity logs for governance and compliance
- **💼 Capacity Management**: View, monitor, and manage Fabric capacities and workspace assignments
- **🔄 Workspace Migration**: Plan and execute workspace migrations with detailed content analysis
- **✏️ Workspace Management**: Rename workspaces, manage users, and perform bulk operations
- **🔐 Secure Authentication**: MSAL-based authentication with Azure AD

## Project Structure

```
.
├── config/                      # Configuration files
│   ├── credentials.json.template # Template for API credentials
│   └── README.md                # Configuration documentation
├── modules/                     # Python utility modules
│   ├── fabric_auth.py          # Authentication module
│   ├── fabric_client.py        # Fabric API client
│   └── utils.py                # Helper utilities
├── notebooks/                   # Jupyter notebooks
│   ├── 00_getting_started.ipynb           # Quick start guide
│   ├── 01_audit_data_collection.ipynb     # Audit data collection
│   ├── 02_capacity_management.ipynb       # Capacity management
│   ├── 03_workspace_migration.ipynb       # Workspace migration
│   └── 04_workspace_management.ipynb      # Workspace operations
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Prerequisites

1. **Azure AD App Registration**
   - Create an app registration in Azure AD
   - Configure API permissions (see below)
   - Generate a client secret

2. **Required API Permissions**
   
   Your app registration needs these Microsoft Power BI Service permissions:
   - `Tenant.Read.All` - Read all tenants
   - `Tenant.ReadWrite.All` - Read and write all tenants
   - `Workspace.Read.All` - Read all workspaces
   - `Workspace.ReadWrite.All` - Read and write all workspaces
   - `Dataset.Read.All` - Read all datasets
   - `Report.Read.All` - Read all reports
   - `Capacity.Read.All` - Read all capacities

3. **Admin Consent**
   - Grant admin consent for the API permissions
   - Ensure you have Fabric/Power BI admin rights

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/villezekeviking/TEest.git
   cd TEest
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**
   ```bash
   cp config/credentials.json.template config/credentials.json
   # Edit config/credentials.json with your Azure AD credentials
   ```

4. **Launch Jupyter**
   ```bash
   jupyter notebook
   ```

## Quick Start

1. Open `notebooks/00_getting_started.ipynb` to test your setup
2. The notebook will verify:
   - Credentials are configured correctly
   - Authentication is working
   - API access is available
   - Basic environment statistics

3. Once setup is confirmed, explore other notebooks for specific tasks

## Notebooks Overview

### 00_getting_started.ipynb
Quick start guide that tests authentication and displays environment overview.

### 01_audit_data_collection.ipynb
- Collect activity logs for specified time periods
- Generate audit reports
- Analyze user activities and operations
- Export audit data to Excel/CSV

### 02_capacity_management.ipynb
- List all Fabric capacities
- View capacity assignments
- Assign workspaces to capacities
- Analyze capacity utilization
- Export capacity reports

### 03_workspace_migration.ipynb
- List workspace contents (datasets, reports, dashboards)
- Create migration plans
- Analyze dependencies
- Document migration steps
- Export migration analysis

### 04_workspace_management.ipynb
- List and filter workspaces
- Rename individual or multiple workspaces
- Create new workspaces
- Manage workspace users and permissions
- Bulk operations with dry-run support
- Export workspace inventory

## Security Best Practices

- ✅ Never commit `credentials.json` to version control
- ✅ Store credentials securely (use Azure Key Vault in production)
- ✅ Rotate client secrets regularly
- ✅ Use least-privilege principle for API permissions
- ✅ Review audit logs regularly
- ✅ Test all operations in non-production environments first

## Usage Examples

### Collecting Audit Data
```python
from modules.fabric_auth import FabricAuth, load_credentials
from modules.fabric_client import FabricClient

credentials = load_credentials('config/credentials.json')
auth = FabricAuth(**credentials)
token = auth.get_access_token()
client = FabricClient(token)

events = client.get_activity_events('2024-01-01T00:00:00', '2024-01-31T23:59:59')
```

### Renaming a Workspace
```python
client.update_workspace(workspace_id='abc123', name='New Workspace Name')
```

### Assigning Workspace to Capacity
```python
client.assign_workspace_to_capacity(workspace_id='abc123', capacity_id='xyz789')
```

## Troubleshooting

### Authentication Fails
- Verify credentials in `config/credentials.json`
- Check that API permissions are granted and admin consent is provided
- Ensure your app registration is active

### No Data Returned
- Verify you have admin access to the Fabric tenant
- Check that workspaces/capacities exist in your tenant
- Review API permission grants

### Module Not Found
- Ensure you're running notebooks from the `notebooks/` directory
- Check that Python path includes parent directory

### Import Errors
- Install all dependencies: `pip install -r requirements.txt`
- Verify Python version compatibility (3.7+)

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing patterns
- Notebooks are well-documented
- Sensitive data is not included
- Tests pass (if applicable)

## License

This project is provided as-is for governance and administration of Microsoft Fabric environments.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review notebook documentation
3. Consult Microsoft Fabric/Power BI API documentation
4. Open an issue on GitHub

## Related Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Power BI REST API Reference](https://learn.microsoft.com/rest/api/power-bi/)
- [MSAL Python Documentation](https://msal-python.readthedocs.io/)
- [Azure AD App Registration Guide](https://learn.microsoft.com/azure/active-directory/develop/quickstart-register-app)
