import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def send_to_power_automate(image_url, region, site, technician_id):
    power_automate_url = "https://algobiz.in.flow.microsoft.com/api/<your-flow-endpoint>"
    headers = {'Content-Type': 'application/json'}
    payload = {
        'image_url': image_url,
        'region': region,
        'site': site,
        'technician_id': technician_id
    }
    response = requests.post(power_automate_url, headers=headers, json=payload)
    return response.json() if response.status_code == 200 else {'error': 'Failed to send to Power Automate'}



@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract image URL and metadata (if available)
        image_url = data.get('image_url')
        region = data.get('region')
        site = data.get('site')
        technician_id = data.get('technician_id')

        # Check if image_url exists and pass to Power Automate flow
        if image_url:
            response = send_to_power_automate(image_url, region, site, technician_id)
            return JsonResponse({'status': 'processed', 'response': response})
        return JsonResponse({'error': 'Image URL not found'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# # image_processing/views.py
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .helpers import get_access_token
# import json

# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         image_url = data.get('image_url')
#         region = data.get('region')
#         site = data.get('site')

#         if image_url:
#             # Download the image
#             image_data = requests.get(image_url).content

#             # Upload to OneDrive
#             response = upload_to_onedrive(image_data, region, site)
#             return JsonResponse(response, safe=False)
#         else:
#             return JsonResponse({'error': 'Image URL not provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# def upload_to_onedrive(image_data, region, site):
#     access_token = get_access_token()
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'image/jpeg'
#     }
#     file_name = f"{region}/{site}/image.jpg"
#     url = f'https://graph.microsoft.com/v1.0/me/drive/items/{settings.MICROSOFT_ONE_DRIVE_FOLDER_ID}:/{file_name}:/content'
#     response = requests.put(url, headers=headers, data=image_data)
#     return response.json()


#-----------------------------------------------------------------------------------------------------------------------------------------------


# import requests
# from django.http import JsonResponse
# from django.views import View
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt

# class UploadImageView(View):
#     @csrf_exempt  # Temporarily exempt from CSRF for testing (not recommended for production)
#     def post(self, request):
#         # Extract image file from request
#         image_file = request.FILES.get('image')
#         if not image_file:
#             return JsonResponse({'error': 'No image provided'}, status=400)

#         # Step 1: Get the access token
#         access_token = self.get_access_token()

#         if not access_token:
#             return JsonResponse({'error': 'Could not obtain access token'}, status=500)

#         # Step 2: Prepare file details for upload
#         file_name = f"region/site/folder/{image_file.name}"  # Adjust as needed

#         # Step 3: Upload file to SharePoint
#         upload_response = self.upload_file_to_sharepoint(access_token, file_name, image_file)

#         return upload_response

#     def get_access_token(self):
#         # Set the Azure AD app credentials
#         client_id = settings.CLIENT_ID
#         client_secret = settings.CLIENT_SECRET
#         tenant_id = settings.TENANT_ID

#         # Set the resource URL and the token URL
#         resource = 'https://graph.microsoft.com/'
#         token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

#         # Prepare the payload for the token request
#         payload = {
#             'client_id': client_id,
#             'client_secret': client_secret,
#             'scope': f"{resource}.default",
#             'grant_type': 'client_credentials',
#         }

#         # Request the access token
#         response = requests.post(token_url, data=payload)

#         if response.status_code == 200:
#             return response.json().get('access_token')
#         else:
#             print("Error obtaining access token:", response.json())
#             return None

#     def upload_file_to_sharepoint(self, access_token, file_name, image_file):
#         # Set the SharePoint site and document library
#         site_id = 'your_site_id'  # Replace with your SharePoint site ID
#         drive_id = 'your_drive_id'  # Replace with your document library ID

#         # URL to upload a file to SharePoint
#         url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/root:/{file_name}:/content"

#         headers = {
#             'Authorization': f'Bearer {access_token}',
#             'Content-Type': 'application/octet-stream'
#         }

#         # Upload the file directly from the InMemoryUploadedFile
#         response = requests.put(url, headers=headers, data=image_file.read())

#         # Check the response
#         if response.status_code in (200, 201):
#             return JsonResponse({'message': 'File uploaded successfully'}, status=200)
#         else:
#             print("Error uploading file:", response.json())
#             return JsonResponse({'error': 'Error uploading file', 'details': response.json()}, status=500)


#---------------------------------------------------------------------------------------------------------------



def upload_to_sharepoint(image_url, region, site, technician_id):
    access_token = get_access_token()
    if not access_token:
        return {'error': 'Could not obtain access token'}

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream'
    }
    
    # Download the image
    image_data = requests.get(image_url).content
    file_name = f"{region}/{site}/{technician_id}/{os.path.basename(image_url)}"
    url = f"https://graph.microsoft.com/v1.0/sites/{settings.MICROSOFT_SITE_ID}/drive/root:/{file_name}:/content"

    response = requests.put(url, headers=headers, data=image_data)
    
    if response.status_code in (200, 201):
        return {'message': 'File uploaded successfully'}
    else:
        return {'error': 'Error uploading file', 'details': response.json()}
