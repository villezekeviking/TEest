# Quick Setup Guide

Follow these steps to get started with the Fabric Governance Toolkit.

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `msal` - Microsoft Authentication Library
- `requests` - HTTP library
- `pandas` - Data analysis library
- `jupyter` - Jupyter notebook server
- `python-dotenv` - Environment variable management
- `openpyxl` - Excel file handling

## Step 2: Configure Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Enter a name (e.g., "Fabric Governance Tool")
5. Select **Accounts in this organizational directory only**
6. Click **Register**

## Step 3: Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Power BI Service**
4. Select **Delegated permissions** or **Application permissions** (recommended)
5. Add these permissions:
   - `Tenant.Read.All`
   - `Tenant.ReadWrite.All`
   - `Workspace.Read.All`
   - `Workspace.ReadWrite.All`
   - `Dataset.Read.All`
   - `Report.Read.All`
   - `Capacity.Read.All`
6. Click **Grant admin consent** (requires admin rights)

## Step 4: Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description and set expiration
4. Click **Add**
5. **Copy the secret value immediately** (you won't see it again!)

## Step 5: Configure Credentials

1. Copy the template:
   ```bash
   cp config/credentials.json.template config/credentials.json
   ```

2. Edit `config/credentials.json` with your values:
   ```json
   {
     "tenant_id": "your-tenant-id-from-azure-ad",
     "client_id": "your-client-id-from-app-registration",
     "client_secret": "your-client-secret-value"
   }
   ```

Where to find these values:
- **tenant_id**: Azure AD > Overview > Tenant ID
- **client_id**: Your app registration > Overview > Application (client) ID
- **client_secret**: The value you copied when creating the secret

## Step 6: Launch Jupyter

```bash
jupyter notebook
```

This will open Jupyter in your browser.

## Step 7: Test Your Setup

1. Navigate to the `notebooks/` directory
2. Open `00_getting_started.ipynb`
3. Run all cells to verify:
   - Authentication works
   - API access is available
   - You can retrieve workspaces and capacities

## Troubleshooting

### Authentication Fails

**Error**: "Authentication failed"

**Solutions**:
- Verify credentials are correct in `config/credentials.json`
- Check that admin consent was granted for API permissions
- Ensure your app registration is active
- Verify tenant_id, client_id, and client_secret are correct

### No Data Returned

**Error**: API calls return empty results or None

**Solutions**:
- Verify you have Fabric/Power BI admin rights in your tenant
- Check that workspaces/capacities actually exist in your environment
- Ensure API permissions are properly granted
- Try the getting started notebook to diagnose the issue

### Module Import Errors

**Error**: `ModuleNotFoundError`

**Solutions**:
- Ensure dependencies are installed: `pip install -r requirements.txt`
- Verify you're running Python 3.7 or higher
- Check that you're running notebooks from the `notebooks/` directory
- Restart the Jupyter kernel after installing packages

### Permission Denied

**Error**: 403 Forbidden or permission errors

**Solutions**:
- Verify admin consent was granted for all required permissions
- Check that your user account has admin rights in Fabric/Power BI
- Ensure the app registration has Application permissions (not just Delegated)
- Wait a few minutes after granting permissions for changes to propagate

## Next Steps

Once setup is complete:

1. **Learn the basics**: Review `notebooks/00_getting_started.ipynb`
2. **Collect audit data**: Use `notebooks/01_audit_data_collection.ipynb`
3. **Manage capacities**: Use `notebooks/02_capacity_management.ipynb`
4. **Plan migrations**: Use `notebooks/03_workspace_migration.ipynb`
5. **Manage workspaces**: Use `notebooks/04_workspace_management.ipynb`

## Security Reminders

- ✅ Never commit `config/credentials.json` to version control
- ✅ Rotate client secrets regularly (every 90 days recommended)
- ✅ Use least-privilege access principle
- ✅ Store credentials securely (consider Azure Key Vault for production)
- ✅ Review audit logs regularly
- ✅ Test all operations in non-production environments first

## Getting Help

- Check the [USAGE.md](USAGE.md) for detailed examples
- Review the [README.md](README.md) for comprehensive documentation
- Consult [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- Review [Power BI REST API docs](https://learn.microsoft.com/rest/api/power-bi/)
