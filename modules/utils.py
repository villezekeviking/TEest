"""
Utility functions for Fabric governance operations.
"""

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


def filter_workspaces_by_name(workspaces: List[Dict], name_pattern: str) -> List[Dict]:
    """
    Filter workspaces by name pattern.
    
    Args:
        workspaces: List of workspace dictionaries
        name_pattern: Pattern to search for in workspace names
        
    Returns:
        Filtered list of workspaces
    """
    return [ws for ws in workspaces if name_pattern.lower() in ws.get('name', '').lower()]


def export_to_excel(data: pd.DataFrame, filename: str, sheet_name: str = 'Sheet1') -> None:
    """
    Export DataFrame to Excel file.
    
    Args:
        data: Pandas DataFrame to export
        filename: Output Excel filename
        sheet_name: Name of the Excel sheet
    """
    data.to_excel(filename, sheet_name=sheet_name, index=False)
    print(f"Data exported to {filename}")


def export_to_csv(data: pd.DataFrame, filename: str) -> None:
    """
    Export DataFrame to CSV file.
    
    Args:
        data: Pandas DataFrame to export
        filename: Output CSV filename
    """
    data.to_csv(filename, index=False)
    print(f"Data exported to {filename}")


def generate_audit_report(events: List[Dict]) -> pd.DataFrame:
    """
    Generate audit report from activity events.
    
    Args:
        events: List of activity event dictionaries
        
    Returns:
        DataFrame containing formatted audit data
    """
    if not events:
        return pd.DataFrame()
    
    df = pd.DataFrame(events)
    
    # Select relevant columns if they exist
    relevant_columns = [
        'CreationTime', 'Operation', 'UserId', 'Activity', 
        'WorkspaceName', 'ItemName', 'DatasetName', 'ReportName'
    ]
    
    existing_columns = [col for col in relevant_columns if col in df.columns]
    
    if existing_columns:
        df = df[existing_columns]
    
    return df


def compare_workspaces(ws1: Dict, ws2: Dict) -> Dict[str, any]:
    """
    Compare two workspaces and return differences.
    
    Args:
        ws1: First workspace dictionary
        ws2: Second workspace dictionary
        
    Returns:
        Dictionary containing differences
    """
    differences = {}
    
    all_keys = set(ws1.keys()) | set(ws2.keys())
    
    for key in all_keys:
        val1 = ws1.get(key)
        val2 = ws2.get(key)
        
        if val1 != val2:
            differences[key] = {
                'workspace1': val1,
                'workspace2': val2
            }
    
    return differences


def validate_workspace_name(name: str) -> bool:
    """
    Validate workspace name according to Fabric rules.
    
    Args:
        name: Proposed workspace name
        
    Returns:
        True if name is valid, False otherwise
    """
    if not name or len(name) == 0:
        return False
    
    if len(name) > 200:
        return False
    
    # Add more validation rules as needed
    return True


def create_migration_plan(source_workspace_id: str, target_workspace_id: str, 
                          items_to_migrate: List[str]) -> Dict:
    """
    Create a migration plan for workspace items.
    
    Args:
        source_workspace_id: Source workspace ID
        target_workspace_id: Target workspace ID
        items_to_migrate: List of item IDs to migrate
        
    Returns:
        Migration plan dictionary
    """
    return {
        'source_workspace': source_workspace_id,
        'target_workspace': target_workspace_id,
        'items': items_to_migrate,
        'created_at': datetime.now().isoformat(),
        'status': 'planned'
    }
