"""
Fabric API Authentication Module

This module handles authentication to Microsoft Fabric APIs using MSAL.
"""

import msal
import json
import os
from typing import Dict, Optional


class FabricAuth:
    """Handle authentication for Microsoft Fabric APIs."""
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        Initialize Fabric authentication.
        
        Args:
            tenant_id: Azure AD tenant ID
            client_id: Application (client) ID
            client_secret: Client secret
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.scope = ["https://analysis.windows.net/powerbi/api/.default"]
        
    def get_access_token(self) -> Optional[str]:
        """
        Get an access token for Fabric API.
        
        Returns:
            Access token string or None if authentication fails
        """
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            print(f"Authentication failed: {result.get('error')}")
            print(f"Error description: {result.get('error_description')}")
            return None


def load_credentials(config_path: str = "config/credentials.json") -> Dict:
    """
    Load credentials from configuration file.
    
    Args:
        config_path: Path to credentials configuration file
        
    Returns:
        Dictionary containing credentials
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Credentials file not found at {config_path}")
