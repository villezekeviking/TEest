# Fabric Governance Configuration

## Authentication Setup

1. Copy `credentials.json.template` to `credentials.json`
2. Fill in your Azure AD credentials:
   - `tenant_id`: Your Azure AD tenant ID
   - `client_id`: Your app registration client ID  
   - `client_secret`: Your app registration client secret

## App Registration Requirements

Your Azure AD app registration needs the following API permissions:
- Microsoft Power BI Service
  - Tenant.Read.All
  - Tenant.ReadWrite.All
  - Workspace.Read.All
  - Workspace.ReadWrite.All
  - Dataset.Read.All
  - Report.Read.All
  - Capacity.Read.All

## Security Notes

- Never commit `credentials.json` to version control
- The file is excluded in `.gitignore`
- Store credentials securely
- Rotate client secrets regularly
