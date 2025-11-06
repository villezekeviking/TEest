"""
Fabric API Client Module

This module provides a client for interacting with Microsoft Fabric APIs.
"""

import requests
from typing import Dict, List, Optional, Any
import pandas as pd


class FabricClient:
    """Client for Microsoft Fabric API operations."""
    
    BASE_URL = "https://api.fabric.microsoft.com/v1"
    POWERBI_URL = "https://api.powerbi.com/v1.0/myorg"
    
    def __init__(self, access_token: str):
        """
        Initialize Fabric client.
        
        Args:
            access_token: OAuth2 access token
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, url: str, **kwargs) -> Optional[Dict]:
        """
        Make HTTP request to Fabric API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            url: Full URL to request
            **kwargs: Additional arguments for requests
            
        Returns:
            Response JSON or None if request fails
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            
            if response.status_code == 204:  # No content
                return {"status": "success"}
            
            return response.json() if response.content else {"status": "success"}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    # Workspace operations
    def get_workspaces(self) -> Optional[List[Dict]]:
        """Get all workspaces."""
        url = f"{self.POWERBI_URL}/groups"
        result = self._make_request("GET", url)
        return result.get("value", []) if result else None
    
    def get_workspace(self, workspace_id: str) -> Optional[Dict]:
        """Get workspace details by ID."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}"
        return self._make_request("GET", url)
    
    def create_workspace(self, name: str) -> Optional[Dict]:
        """Create a new workspace."""
        url = f"{self.POWERBI_URL}/groups"
        data = {"name": name}
        return self._make_request("POST", url, json=data)
    
    def update_workspace(self, workspace_id: str, name: str) -> Optional[Dict]:
        """Update workspace name."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}"
        data = {"name": name}
        return self._make_request("PATCH", url, json=data)
    
    def delete_workspace(self, workspace_id: str) -> Optional[Dict]:
        """Delete a workspace."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}"
        return self._make_request("DELETE", url)
    
    # Capacity operations
    def get_capacities(self) -> Optional[List[Dict]]:
        """Get all capacities."""
        url = f"{self.POWERBI_URL}/capacities"
        result = self._make_request("GET", url)
        return result.get("value", []) if result else None
    
    def assign_workspace_to_capacity(self, workspace_id: str, capacity_id: str) -> Optional[Dict]:
        """Assign workspace to a capacity."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}/AssignToCapacity"
        data = {"capacityId": capacity_id}
        return self._make_request("POST", url, json=data)
    
    # Dataset and Report operations
    def get_datasets(self, workspace_id: str) -> Optional[List[Dict]]:
        """Get all datasets in a workspace."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}/datasets"
        result = self._make_request("GET", url)
        return result.get("value", []) if result else None
    
    def get_reports(self, workspace_id: str) -> Optional[List[Dict]]:
        """Get all reports in a workspace."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}/reports"
        result = self._make_request("GET", url)
        return result.get("value", []) if result else None
    
    def get_dashboards(self, workspace_id: str) -> Optional[List[Dict]]:
        """Get all dashboards in a workspace."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}/dashboards"
        result = self._make_request("GET", url)
        return result.get("value", []) if result else None
    
    # Activity logs for audit
    def get_activity_events(self, start_datetime: str, end_datetime: str) -> Optional[List[Dict]]:
        """
        Get activity events for audit.
        
        Args:
            start_datetime: Start datetime in ISO format (e.g., '2024-01-01T00:00:00')
            end_datetime: End datetime in ISO format
            
        Returns:
            List of activity events
        """
        url = f"{self.POWERBI_URL}/admin/activityevents"
        params = {
            "startDateTime": f"'{start_datetime}'",
            "endDateTime": f"'{end_datetime}'"
        }
        result = self._make_request("GET", url, params=params)
        return result.get("activityEventEntities", []) if result else None
    
    # User and permissions
    def get_workspace_users(self, workspace_id: str) -> Optional[List[Dict]]:
        """Get users in a workspace."""
        url = f"{self.POWERBI_URL}/groups/{workspace_id}/users"
        result = self._make_request("GET", url)
        return result.get("value", []) if result else None
    
    def add_workspace_user(self, workspace_id: str, email: str, access_right: str = "Member") -> Optional[Dict]:
        """
        Add user to workspace.
        
        Args:
            workspace_id: Workspace ID
            email: User email
            access_right: Access level (Admin, Member, Contributor, Viewer)
        """
        url = f"{self.POWERBI_URL}/groups/{workspace_id}/users"
        data = {
            "emailAddress": email,
            "groupUserAccessRight": access_right
        }
        return self._make_request("POST", url, json=data)


def workspaces_to_dataframe(workspaces: List[Dict]) -> pd.DataFrame:
    """Convert workspaces list to pandas DataFrame."""
    if not workspaces:
        return pd.DataFrame()
    return pd.DataFrame(workspaces)


def capacities_to_dataframe(capacities: List[Dict]) -> pd.DataFrame:
    """Convert capacities list to pandas DataFrame."""
    if not capacities:
        return pd.DataFrame()
    return pd.DataFrame(capacities)
