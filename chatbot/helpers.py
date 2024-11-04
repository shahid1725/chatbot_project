def get_access_token():
    client_id = settings.MICROSOFT_CLIENT_ID
    client_secret = settings.MICROSOFT_CLIENT_SECRET
    tenant_id = settings.MICROSOFT_TENANT_ID
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials',
    }
    
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Error obtaining access token:", response.json())
        return None

