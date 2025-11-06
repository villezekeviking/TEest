# Fabric Governance Toolkit - Usage Examples

This document provides detailed usage examples for the Fabric Governance Toolkit.

## Table of Contents

1. [Setup and Authentication](#setup-and-authentication)
2. [Audit Data Collection](#audit-data-collection)
3. [Capacity Management](#capacity-management)
4. [Workspace Operations](#workspace-operations)
5. [Advanced Scenarios](#advanced-scenarios)

---

## Setup and Authentication

### Initial Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Credentials**
   ```bash
   cp config/credentials.json.template config/credentials.json
   ```

3. **Edit credentials.json**
   ```json
   {
     "tenant_id": "your-tenant-id",
     "client_id": "your-client-id",
     "client_secret": "your-client-secret"
   }
   ```

### Authentication Example

```python
from modules.fabric_auth import FabricAuth, load_credentials
from modules.fabric_client import FabricClient

# Load credentials from config file
credentials = load_credentials('config/credentials.json')

# Create authentication instance
auth = FabricAuth(
    tenant_id=credentials['tenant_id'],
    client_id=credentials['client_id'],
    client_secret=credentials['client_secret']
)

# Get access token
token = auth.get_access_token()

# Create Fabric client
client = FabricClient(token)
```

---

## Audit Data Collection

### Collect Last 7 Days of Activity

```python
from datetime import datetime, timedelta
from modules.utils import generate_audit_report, export_to_excel

# Define time range
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

start_datetime = start_date.strftime('%Y-%m-%dT%H:%M:%S')
end_datetime = end_date.strftime('%Y-%m-%dT%H:%M:%S')

# Get activity events
events = client.get_activity_events(start_datetime, end_datetime)

# Generate report
audit_df = generate_audit_report(events)

# Export to Excel
export_to_excel(audit_df, 'audit_report_7days.xlsx', 'Audit Data')
```

### Analyze User Activities

```python
import pandas as pd

# Get activity events
events = client.get_activity_events('2024-01-01T00:00:00', '2024-01-31T23:59:59')
audit_df = pd.DataFrame(events)

# Most active users
if 'UserId' in audit_df.columns:
    top_users = audit_df['UserId'].value_counts().head(10)
    print("Most Active Users:")
    print(top_users)

# Most common operations
if 'Operation' in audit_df.columns:
    top_operations = audit_df['Operation'].value_counts().head(10)
    print("\nMost Common Operations:")
    print(top_operations)
```

---

## Capacity Management

### List All Capacities

```python
from modules.fabric_client import capacities_to_dataframe

# Get capacities
capacities = client.get_capacities()
capacities_df = capacities_to_dataframe(capacities)

print(f"Found {len(capacities)} capacities")
print(capacities_df)
```

### Assign Workspace to Capacity

```python
workspace_id = "abc-123-def-456"
capacity_id = "xyz-789-uvw-012"

result = client.assign_workspace_to_capacity(workspace_id, capacity_id)
if result:
    print(f"✓ Workspace assigned to capacity successfully")
else:
    print(f"✗ Failed to assign workspace")
```

### Analyze Capacity Usage

```python
from modules.fabric_client import workspaces_to_dataframe

# Get all workspaces
workspaces = client.get_workspaces()
workspaces_df = workspaces_to_dataframe(workspaces)

# Group by capacity
if 'capacityId' in workspaces_df.columns:
    capacity_usage = workspaces_df.groupby('capacityId').size()
    print("Workspaces per Capacity:")
    print(capacity_usage)
    
    # Find unassigned workspaces
    unassigned = workspaces_df[workspaces_df['capacityId'].isna()]
    print(f"\nUnassigned workspaces: {len(unassigned)}")
```

---

## Workspace Operations

### List and Filter Workspaces

```python
from modules.utils import filter_workspaces_by_name

# Get all workspaces
workspaces = client.get_workspaces()
print(f"Total workspaces: {len(workspaces)}")

# Filter by name pattern
dev_workspaces = filter_workspaces_by_name(workspaces, "dev")
print(f"Development workspaces: {len(dev_workspaces)}")

for ws in dev_workspaces:
    print(f"  - {ws['name']} ({ws['id']})")
```

### Rename a Workspace

```python
from modules.utils import validate_workspace_name

workspace_id = "abc-123-def-456"
new_name = "Production - Sales Analytics"

# Validate name first
if validate_workspace_name(new_name):
    result = client.update_workspace(workspace_id, new_name)
    if result:
        print(f"✓ Workspace renamed to '{new_name}'")
    else:
        print(f"✗ Failed to rename workspace")
else:
    print(f"✗ Invalid workspace name")
```

### Create New Workspace

```python
workspace_name = "New Analytics Workspace"

if validate_workspace_name(workspace_name):
    result = client.create_workspace(workspace_name)
    if result:
        print(f"✓ Workspace created: {result.get('id')}")
    else:
        print(f"✗ Failed to create workspace")
```

### Bulk Rename Workspaces

```python
def bulk_rename_add_prefix(workspaces, prefix, dry_run=True):
    """Add prefix to multiple workspaces."""
    results = []
    
    for ws in workspaces:
        old_name = ws['name']
        new_name = f"{prefix}{old_name}"
        
        if validate_workspace_name(new_name):
            if dry_run:
                print(f"Would rename: '{old_name}' -> '{new_name}'")
                results.append({'success': True, 'workspace_id': ws['id']})
            else:
                result = client.update_workspace(ws['id'], new_name)
                if result:
                    print(f"✓ Renamed: '{old_name}' -> '{new_name}'")
                    results.append({'success': True, 'workspace_id': ws['id']})
                else:
                    print(f"✗ Failed: '{old_name}'")
                    results.append({'success': False, 'workspace_id': ws['id']})
    
    return results

# Example: Add "PROD_" prefix to all production workspaces
prod_workspaces = filter_workspaces_by_name(workspaces, "production")
bulk_rename_add_prefix(prod_workspaces, "PROD_", dry_run=True)
```

### Manage Workspace Users

```python
workspace_id = "abc-123-def-456"

# Get current users
users = client.get_workspace_users(workspace_id)
print(f"Current users: {len(users)}")

# Add a new user
result = client.add_workspace_user(
    workspace_id=workspace_id,
    email="user@example.com",
    access_right="Member"  # Options: Admin, Member, Contributor, Viewer
)

if result:
    print("✓ User added successfully")
```

---

## Advanced Scenarios

### Workspace Migration Planning

```python
from modules.utils import create_migration_plan

# Get source workspace content
source_id = "source-workspace-id"
target_id = "target-workspace-id"

# Get all items from source
datasets = client.get_datasets(source_id)
reports = client.get_reports(source_id)
dashboards = client.get_dashboards(source_id)

# Collect item IDs
items_to_migrate = []
items_to_migrate.extend([ds['id'] for ds in datasets])
items_to_migrate.extend([rpt['id'] for rpt in reports])

# Create migration plan
plan = create_migration_plan(source_id, target_id, items_to_migrate)

# Save plan
import json
with open('migration_plan.json', 'w') as f:
    json.dump(plan, f, indent=2)

print(f"✓ Migration plan created with {len(items_to_migrate)} items")
```

### Generate Comprehensive Report

```python
from datetime import datetime
import pandas as pd

# Collect all data
workspaces = client.get_workspaces()
capacities = client.get_capacities()

# Generate timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Create Excel workbook with multiple sheets
filename = f'fabric_governance_report_{timestamp}.xlsx'

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    # Workspaces sheet
    ws_df = pd.DataFrame(workspaces)
    ws_df.to_excel(writer, sheet_name='Workspaces', index=False)
    
    # Capacities sheet
    cap_df = pd.DataFrame(capacities)
    cap_df.to_excel(writer, sheet_name='Capacities', index=False)
    
    # Summary sheet
    summary = pd.DataFrame({
        'Metric': ['Total Workspaces', 'Total Capacities', 'Generated'],
        'Value': [len(workspaces), len(capacities), timestamp]
    })
    summary.to_excel(writer, sheet_name='Summary', index=False)

print(f"✓ Report generated: {filename}")
```

### Audit Compliance Check

```python
from datetime import datetime, timedelta

# Define compliance period (last 30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Get activity events
events = client.get_activity_events(
    start_date.strftime('%Y-%m-%dT%H:%M:%S'),
    end_date.strftime('%Y-%m-%dT%H:%M:%S')
)

# Analyze for compliance
df = pd.DataFrame(events)

# Check for sensitive operations
if 'Operation' in df.columns:
    sensitive_ops = ['DeleteWorkspace', 'DeleteDataset', 'DeleteReport']
    sensitive_events = df[df['Operation'].isin(sensitive_ops)]
    
    print(f"Sensitive operations in last 30 days: {len(sensitive_events)}")
    
    if len(sensitive_events) > 0:
        print("\nSensitive Operations:")
        print(sensitive_events[['CreationTime', 'Operation', 'UserId', 'WorkspaceName']])
```

### Workspace Health Check

```python
def workspace_health_check(workspace_id):
    """Perform health check on a workspace."""
    
    print(f"=== Health Check for Workspace {workspace_id} ===\n")
    
    # Get workspace details
    workspace = client.get_workspace(workspace_id)
    if not workspace:
        print("✗ Workspace not found")
        return
    
    print(f"Name: {workspace.get('name')}")
    print(f"Type: {workspace.get('type')}")
    print(f"State: {workspace.get('state')}")
    
    # Check capacity assignment
    if workspace.get('capacityId'):
        print(f"✓ Assigned to capacity: {workspace['capacityId']}")
    else:
        print("⚠ Not assigned to any capacity")
    
    # Check content
    datasets = client.get_datasets(workspace_id)
    reports = client.get_reports(workspace_id)
    dashboards = client.get_dashboards(workspace_id)
    
    print(f"\nContent:")
    print(f"  Datasets: {len(datasets) if datasets else 0}")
    print(f"  Reports: {len(reports) if reports else 0}")
    print(f"  Dashboards: {len(dashboards) if dashboards else 0}")
    
    # Check users
    users = client.get_workspace_users(workspace_id)
    if users:
        print(f"\nUsers: {len(users)}")
        admin_count = sum(1 for u in users if u.get('groupUserAccessRight') == 'Admin')
        print(f"  Admins: {admin_count}")
    
    print("\n✓ Health check complete")

# Run health check
workspace_health_check("your-workspace-id")
```

---

## Tips and Best Practices

1. **Always use dry_run mode** when performing bulk operations
2. **Export data regularly** for backup and auditing purposes
3. **Test in non-production** environments first
4. **Monitor API rate limits** when processing large datasets
5. **Validate names** before renaming operations
6. **Document migrations** using the migration plan feature
7. **Review audit logs** regularly for compliance
8. **Secure credentials** - never commit credentials.json to version control

---

## Error Handling

### Robust Error Handling Pattern

```python
from modules.fabric_auth import FabricAuth, load_credentials
from modules.fabric_client import FabricClient

try:
    # Load credentials
    credentials = load_credentials('config/credentials.json')
    
    # Authenticate
    auth = FabricAuth(**credentials)
    token = auth.get_access_token()
    
    if not token:
        raise Exception("Failed to obtain access token")
    
    # Create client
    client = FabricClient(token)
    
    # Perform operations
    workspaces = client.get_workspaces()
    if workspaces:
        print(f"✓ Retrieved {len(workspaces)} workspaces")
    else:
        print("⚠ No workspaces retrieved")
        
except FileNotFoundError:
    print("✗ Credentials file not found")
    print("Please copy credentials.json.template to credentials.json")
except Exception as e:
    print(f"✗ Error: {e}")
```

---

## Additional Resources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Power BI REST API Reference](https://learn.microsoft.com/rest/api/power-bi/)
- [Azure AD App Permissions](https://learn.microsoft.com/azure/active-directory/develop/v2-permissions-and-consent)
