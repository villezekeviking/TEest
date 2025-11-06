"""
Fabric Governance Toolkit

A comprehensive Python library for managing Microsoft Fabric environments.
"""

__version__ = "1.0.0"

from .fabric_auth import FabricAuth, load_credentials
from .fabric_client import FabricClient, workspaces_to_dataframe, capacities_to_dataframe
from .utils import (
    filter_workspaces_by_name,
    export_to_excel,
    export_to_csv,
    generate_audit_report,
    validate_workspace_name,
    create_migration_plan
)

__all__ = [
    'FabricAuth',
    'FabricClient',
    'load_credentials',
    'workspaces_to_dataframe',
    'capacities_to_dataframe',
    'filter_workspaces_by_name',
    'export_to_excel',
    'export_to_csv',
    'generate_audit_report',
    'validate_workspace_name',
    'create_migration_plan'
]
