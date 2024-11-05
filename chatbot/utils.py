import requests
import msal
from datetime import datetime

class MicrosoftAuthHandler:
    def __init__(self, client_id, client_secret, tenant_id, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.scope = scope
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"

    def get_access_token(self):
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_silent(self.scope, account=None)
        if not result:
            result = app.acquire_token_for_client(scopes=self.scope)
        
        if "access_token" in result:
            return result['access_token']
        return None

class PowerAutomateHandler:
    def __init__(self, flow_url, auth_handler):
        self.flow_url = flow_url
        self.auth_handler = auth_handler

    def trigger_flow(self, image_data, metadata):
        access_token = self.auth_handler.get_access_token()
        if not access_token:
            raise Exception("Failed to get access token")

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'image_data': image_data,
            'metadata': metadata
        }

        response = requests.post(
            self.flow_url,
            json=payload,
            headers=headers
        )
        return response.json()


#----------------------------------------------------------------------------


def trigger_power_automate_flow(tracking_id, image_file, metadata):
    """
    Trigger Power Automate flow with image and metadata
    """
    headers = {
        'Authorization': f'Bearer {settings.POWER_AUTOMATE_TOKEN}'
    }
    
    files = {
        'image': (image_file.name, image_file, image_file.content_type)
    }
    
    data = {
        'tracking_id': str(tracking_id),
        **metadata,
        'callback_url': f"{settings.BASE_URL}/api/power-automate-callback/"
    }
    
    response = requests.post(
        settings.POWER_AUTOMATE_FLOW_URL,
        headers=headers,
        data=data,
        files=files
    )
    
    return response.json()

def verify_file_in_sharepoint(sharepoint_url):
    """
    Verify file exists in SharePoint using Microsoft Graph API
    """
    headers = {
        'Authorization': f'Bearer {get_graph_api_token()}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{settings.GRAPH_API_BASE_URL}/v1.0/drives/{settings.DRIVE_ID}/items/{get_item_id(sharepoint_url)}",
        headers=headers
    )
    
    return response.json()