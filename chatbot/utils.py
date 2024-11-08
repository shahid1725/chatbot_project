

#----------------------------------------------------------------------------------
import requests
import time
from django.core.cache import cache

# class TokenManager:
#     def __init__(self, client_id, client_secret, tenant_id):
#         self.client_id = client_id
#         self.client_secret = client_secret
#         self.tenant_id = tenant_id
#         self.token = None
#         self.token_expiry = 0

#     def get_new_token(self):
#         """Request a new token using client credentials."""
#         url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
#         headers = {
#             'Content-Type': 'application/x-www-form-urlencoded',
#         }
#         data = {
#             'grant_type': 'client_credentials',
#             'client_id': self.client_id,
#             'client_secret': self.client_secret,
#             'scope': 'https://graph.microsoft.com/.default',
#         }

#         response = requests.post(url, headers=headers, data=data)
#         if response.status_code == 200:
#             token_data = response.json()
#             self.token = token_data['access_token']
#             self.token_expiry = time.time() + token_data['expires_in']  # Store expiry time
#             return self.token
#         else:
#             raise Exception("Failed to obtain access token: " + response.text)

#     def get_token(self):
#         """Check if token is expired or close to expiration, and refresh if needed."""
#         # First check cache for token (cache expiration could be set based on the expiry time)
#         cached_token = cache.get('access_token')
#         if cached_token:
#             return cached_token

#         if self.token is None or time.time() >= self.token_expiry:
#             # Get new token
#             new_token = self.get_new_token()
#             cache.set('access_token', new_token, timeout=self.token_expiry - time.time())  # Cache for token expiry duration
#             return new_token
#         else:
#             return self.token
