# import json
# import requests
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.conf import settings


# def send_to_power_automate(image_url, region, site, technician_id):
#     power_automate_url = "https://algobiz.in.flow.microsoft.com/api/<your-flow-endpoint>"
#     headers = {'Content-Type': 'application/json'}
#     payload = {
#         'image_url': image_url,
#         'region': region,
#         'site': site,
#         'technician_id': technician_id
#     }
#     response = requests.post(power_automate_url, headers=headers, json=payload)
#     return response.json() if response.status_code == 200 else {'error': 'Failed to send to Power Automate'}

# @csrf_exempt
# def whatsapp_webhook(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         image_url = data.get('image_url')
#         region = data.get('region')
#         site = data.get('site')
#         technician_id = data.get('technician_id')

#         if image_url:
#             response = send_to_power_automate(image_url, region, site, technician_id)
#             return JsonResponse({'status': 'processed', 'response': response})
#         return JsonResponse({'error': 'Image URL not found'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         image_url = data.get('image_url')
#         region = data.get('region')
#         site = data.get('site')

#         if image_url:
#             image_data = requests.get(image_url).content
#             response = upload_to_onedrive(image_data, region, site)
#             return JsonResponse(response, safe=False)
#         else:
#             return JsonResponse({'error': 'Image URL not provided'}, status=400)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# def upload_to_onedrive(image_data, region, site):
#     access_token = get_access_token()
#     if not access_token:
#         return {'error': 'Failed to obtain access token'}

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'image/jpeg'
#     }
#     file_name = f"{region}/{site}/image.jpg"
#     user_id = "<user_id>"  # Replace with the actual OneDrive user ID
#     url = f'https://graph.microsoft.com/v1.0/users/{user_id}/drive/root:/{file_name}:/content'

#     response = requests.put(url, headers=headers, data=image_data)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print("Error uploading to OneDrive:", response.json())
#         return {'error': 'Failed to upload to OneDrive', 'details': response.json()}

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



# def upload_to_sharepoint(image_url, region, site, technician_id):
#     access_token = get_access_token()
#     if not access_token:
#         return {'error': 'Could not obtain access token'}

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/octet-stream'
#     }
    
#     # Download the image
#     image_data = requests.get(image_url).content
#     file_name = f"{region}/{site}/{technician_id}/{os.path.basename(image_url)}"
#     url = f"https://graph.microsoft.com/v1.0/sites/{settings.MICROSOFT_SITE_ID}/drive/root:/{file_name}:/content"

#     response = requests.put(url, headers=headers, data=image_data)
    
#     if response.status_code in (200, 201):
#         return {'message': 'File uploaded successfully'}
#     else:
#         return {'error': 'Error uploading file', 'details': response.json()}


#------------------------------------------------------------------------------------------------------------------
# image_transfer/views.py
# import base64
# import requests
# from django.http import JsonResponse
# from django.views import View
# from .models import ImageTransfer  # Import the model

# class UploadImageView(View):
#     def post(self, request):
#         # Extract data from request
#         region = request.POST.get('region')
#         site = request.POST.get('site')
#         folder = request.POST.get('folder')
#         image = request.FILES.get('image')

#         if not image:
#             return JsonResponse({'error': 'No image provided'}, status=400)

#         # Encode the image to base64
#         image_data = base64.b64encode(image.read()).decode('utf-8')

#         # Prepare the data to send to Power Automate
#         flow_url = settings.POWER_AUTOMATE_FLOW_URL  # Replace with your flow URL
#         data = {
#             'region': region,
#             'site': site,
#             'folder': folder,
#             'image_name': image.name,
#             'image': image_data  # Use the base64 encoded image data
#         }

#         # Send the request to Power Automate
#         response = requests.post(flow_url, json=data)

#         if response.status_code == 200:
#             # Log the image transfer (optional)
#             ImageTransfer.objects.create(
#                 image_url=response.json().get('image_url'),
#                 region=region,
#                 site=site,
#                 folder=folder
#             )
#             return JsonResponse({'message': 'Image uploaded successfully'}, status=200)
#         else:
#             return JsonResponse({'error': 'Failed to upload image'}, status=response.status_code)


#-------------------------------------------------------------------------------------------------------------------



from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import base64

class WhatsAppWebhookViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            # Extract image and metadata from WhatsApp message
            image_data = request.data.get('image')
            metadata = {
                'region': request.data.get('region'),
                'site': request.data.get('site'),
                'folder': request.data.get('folder'),
                'timestamp': datetime.now().isoformat()
            }

            # Create ImageUpload instance
            image_upload = ImageUpload.objects.create(
                image=image_data,
                region=metadata['region'],
                site=metadata['site'],
                folder=metadata['folder']
            )

            # Initialize handlers
            auth_handler = MicrosoftAuthHandler(
                settings.MICROSOFT_CLIENT_ID,
                settings.MICROSOFT_CLIENT_SECRET,
                settings.MICROSOFT_TENANT_ID,
                settings.MICROSOFT_GRAPH_SCOPE
            )

            power_automate_handler = PowerAutomateHandler(
                settings.POWER_AUTOMATE_FLOW_URL,
                auth_handler
            )

            # Trigger Power Automate flow
            result = power_automate_handler.trigger_flow(
                base64.b64encode(image_data.read()).decode(),
                metadata
            )

            # Update ImageUpload with SharePoint URL if available
            if 'sharepoint_url' in result:
                image_upload.sharepoint_url = result['sharepoint_url']
                image_upload.processed = True
                image_upload.save()

            return Response({
                'status': 'success',
                'message': 'Image processed successfully',
                'sharepoint_url': result.get('sharepoint_url')
            })

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=500)





# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
import base64

@csrf_exempt
@api_view(['POST'])
def whatsapp_webhook1(request):
    """
    Enhanced webhook endpoint with detailed response for testing
    """
    try:
        # Extract data from request
        image = request.FILES.get('image')
        data = {
            'region': request.POST.get('region'),
            'site': request.POST.get('site'),
            'folder': request.POST.get('folder'),
        }

        # Validate required fields
        required_fields = ['region', 'site', 'folder']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'status': 'error',
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'received_data': data
            }, status=400)

        if not image:
            return JsonResponse({
                'status': 'error',
                'message': 'No image file received',
                'received_data': data
            }, status=400)

        # Process the image (mock processing for testing)
        image_info = {
            'name': image.name,
            'size': image.size,
            'content_type': image.content_type
        }

        # Mock SharePoint URL for testing
        sharepoint_url = f"https://sharepoint.example.com/{data['region']}/{data['site']}/{data['folder']}/{image.name}"

        return JsonResponse({
            'status': 'success',
            'message': 'Image received and processed successfully',
            'data': {
                'metadata': data,
                'image_info': image_info,
                'sharepoint_url': sharepoint_url,
                'timestamp': datetime.now().isoformat()
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=500)



@api_view(['GET'])
def test_connection(request):
    """
    Simple endpoint to test API connectivity
    """
    return Response({
        'status': 'online',
        'message': 'API is working correctly',
        'timestamp': datetime.now().isoformat()
    })


#-------------------------------------------------------------------


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import requests
from .models import ImageTracking
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def whatsapp_webhook(request):
    """
    Webhook endpoint for WhatsApp images
    """
    try:
        # Create tracking record
        tracking = ImageTracking.objects.create(
            whatsapp_message_id=request.data.get('message_id'),
            image_name=request.FILES['image'].name,
            region=request.POST['region'],
            site=request.POST['site'],
            folder=request.POST['folder']
        )

        logger.info(f"Created tracking record: {tracking.tracking_id}")

        # Trigger Power Automate flow
        power_automate_response = trigger_power_automate_flow(
            tracking.tracking_id,
            request.FILES['image'],
            {
                'region': request.POST['region'],
                'site': request.POST['site'],
                'folder': request.POST['folder']
            }
        )

        # Update tracking with Power Automate flow ID
        tracking.power_automate_flow_id = power_automate_response.get('flow_id')
        tracking.status = 'PROCESSING'
        tracking.save()

        return Response({
            'status': 'success',
            'tracking_id': tracking.tracking_id,
            'message': 'Image processing initiated'
        })

    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def power_automate_callback(request):
    """
    Callback endpoint for Power Automate to update status
    """
    tracking_id = request.data.get('tracking_id')
    tracking = get_object_or_404(ImageTracking, tracking_id=tracking_id)

    if request.data.get('status') == 'success':
        tracking.status = 'UPLOADED'
        tracking.sharepoint_url = request.data.get('sharepoint_url')
    else:
        tracking.status = 'FAILED'
        tracking.error_message = request.data.get('error_message')

    tracking.save()
    return Response({'status': 'success'})


@api_view(['GET'])
def check_status(request, tracking_id):
    """
    Check the status of an image upload
    """
    tracking = get_object_or_404(ImageTracking, tracking_id=tracking_id)
    
    return Response({
        'tracking_id': tracking.tracking_id,
        'status': tracking.status,
        'timeline': {
            'received_at': tracking.created_at,
            'last_updated': tracking.updated_at
        },
        'image_details': {
            'name': tracking.image_name,
            'region': tracking.region,
            'site': tracking.site,
            'folder': tracking.folder
        },
        'sharepoint_url': tracking.sharepoint_url if tracking.status == 'UPLOADED' else None,
        'error_message': tracking.error_message if tracking.status == 'FAILED' else None
    })


@api_view(['GET'])
def verify_sharepoint(request, tracking_id):
    """
    Verify if the image exists in SharePoint
    """
    tracking = get_object_or_404(ImageTracking, tracking_id=tracking_id)
    
    if not tracking.sharepoint_url:
        return Response({
            'status': 'error',
            'message': 'SharePoint URL not available'
        }, status=status.HTTP_404_NOT_FOUND)

    # Verify file in SharePoint using Microsoft Graph API
    try:
        graph_response = verify_file_in_sharepoint(tracking.sharepoint_url)
        return Response({
            'status': 'success',
            'exists_in_sharepoint': True,
            'file_details': graph_response
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#-------------------------------------------------------------------------------


# views.py
import requests
import base64
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ImageUpload
from decouple import config

class UploadImageView(APIView):
    def post(self, request):
        # Extract data from the request
        region = request.data.get('region')
        site = request.data.get('site')
        folder = request.data.get('folder')
        image_file = request.FILES.get('image')

        if not image_file:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate a unique filename and save the image
        image_name = f"{region}/{site}/{folder}/{image_file.name}"  # Adjust the path as needed
        path = default_storage.save(image_name, ContentFile(image_file.read()))

        # Construct the full URL for the image
        image_path = default_storage.url(path)

        # Create a new ImageUpload instance
        image_upload = ImageUpload.objects.create(
            region=region,
            site=site,
            folder=folder,
            image_name=image_file.name,
            image_path=image_path
        )

        # Create a response object with image details
        response_data = {
            "id": image_upload.id,
            "region": region,
            "site": site,
            "folder": folder,
            "image_name": image_file.name,
            "image_path": image_path,
            "uploaded_at": timezone.now().isoformat()  # Current timestamp
        }

        # Call the functions to send the image via WhatsApp and to Power Automate
        self.send_image_via_whatsapp(response_data)
        self.send_image_to_power_automate(response_data)

        return Response(response_data, status=status.HTTP_201_CREATED)

    def send_image_via_whatsapp(self, data):
        url = "https://app-server.wati.io/v1/sendImage"  # WATI API endpoint
        
        headers = {
            'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJkNTVjMWYwNi03ZDY1LTQ2ZTktYWY1MS1iNzlmNDQ3MTNkZjkiLCJ1bmlxdWVfbmFtZSI6InNoYWhpZHZhbGl5YWRldkBnbWFpbC5jb20iLCJuYW1laWQiOiJzaGFoaWR2YWxpeWFkZXZAZ21haWwuY29tIiwiZW1haWwiOiJzaGFoaWR2YWxpeWFkZXZAZ21haWwuY29tIiwiYXV0aF90aW1lIjoiMTEvMDUvMjAyNCAxMToyMDo0NyIsImRiX25hbWUiOiJ3YXRpX2FwcF90cmlhbCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6IlRSSUFMIiwiZXhwIjoxNzMxNDU2MDAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.kxgpR42MJNvbbbN4irQycuzWXzkeKDZTN4b5xbkeN9U",  # Ensure the token is set correctly
            'Content-Type': 'application/json',
        }
        payload = {
            "phone": "9995591725",  # Replace with the recipient's phone number
            "image": data['image_path'],  # URL of the image
            "caption": f"Image from {data['region']} - {data['site']}/{data['folder']}"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            json_response = response.json()  # Attempt to decode the response
            print("WhatsApp JSON Response:", json_response)  # Log the decoded JSON response
        except requests.ConnectionError as ce:
            print("Connection error occurred:", ce)
        except requests.Timeout as te:
            print("Request timed out:", te)
        except requests.RequestException as re:
            print("Error occurred while sending request to WhatsApp:", re)
        except ValueError as ve:
            print("Value error:", ve)

    def send_image_to_power_automate(self, data):
        # Construct the Power Automate URL here
        power_automate_url = 'https://prod-16.centralindia.logic.azure.com:443/workflows/c1f3aef5f1574679a11f55bf90924495/triggers/manual/paths/invoke?api-version=2016-06-01'  # Replace with your flow URL

        headers = {
        'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJub25jZSI6IkZYRnpkV2c4ZjRGQUYyN3dXTS02ZElwLXdSTmIzVHdIMEpoMjgza3JuWnMiLCJhbGciOiJSUzI1NiIsIng1dCI6IjNQYUs0RWZ5Qk5RdTNDdGpZc2EzWW1oUTVFMCIsImtpZCI6IjNQYUs0RWZ5Qk5RdTNDdGpZc2EzWW1oUTVFMCJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9mZTJjN2YwMy01ZTZjLTQ1YTUtOTkzZi0zMWIwODgwZWFkMjAvIiwiaWF0IjoxNzMwNzk3NTI1LCJuYmYiOjE3MzA3OTc1MjUsImV4cCI6MTczMDgwMTQyNSwiYWlvIjoiazJCZ1lDZ09xcEY2eWJ2YmJjdFdPMldHZHVFZ0FBPT0iLCJhcHBfZGlzcGxheW5hbWUiOiJjaGF0Ym90IiwiYXBwaWQiOiJhMGVlYjczZi1jZjUwLTQ1ZmUtOWUzZi05OWRhYWM5MjE0MWYiLCJhcHBpZGFjciI6IjEiLCJpZHAiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC9mZTJjN2YwMy01ZTZjLTQ1YTUtOTkzZi0zMWIwODgwZWFkMjAvIiwiaWR0eXAiOiJhcHAiLCJvaWQiOiIzZWU0MTYzYy1kMjAyLTQwZmUtYTEyZC0zNDk2NzhkMTJiNTciLCJyaCI6IjEuQWI0QUEzOHNfbXhlcFVXWlB6R3dpQTZ0SUFNQUFBQUFBQUFBd0FBQUFBQUFBQUMtQUFDLUFBLiIsInN1YiI6IjNlZTQxNjNjLWQyMDItNDBmZS1hMTJkLTM0OTY3OGQxMmI1NyIsInRlbmFudF9yZWdpb25fc2NvcGUiOiJBUyIsInRpZCI6ImZlMmM3ZjAzLTVlNmMtNDVhNS05OTNmLTMxYjA4ODBlYWQyMCIsInV0aSI6InhFZ0g0Wlg4b1VDVEZSVHB5MVlIQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjA5OTdhMWQwLTBkMWQtNGFjYi1iNDA4LWQ1Y2E3MzEyMWU5MCJdLCJ4bXNfaWRyZWwiOiIyNCA3IiwieG1zX3RjZHQiOjE3MzA3OTE1ODF9.MCFAU6Zdlco5TgM6FxSf0lC_e6U_lVQglAfk0GpSuV1sGVdD_taYF1vECHbaP0GqjryEq39Q_CbMfdQgp6eRT8-JJP-P97UEQ8U502r1qYRc6rVBqIaBOb97z8iritCA0E5qN2Qe6Gb_xReLf1X_9CDuoKRkOz2m4cTl00zWnke7CmL_3ChWNO4tNv14cgs7MUn5Y2nqWG6TkPIKI1rXzGTM516qUNDq4qN5lMJ2cZW61WNjFd6Au4mRXvNWMep0_bzr-IPNjxNHJDEnjwGzx0yaw1MkupOTWN4vyHXrfsNPcYZu_BO1_eWmr7bhwtJuYuoy7xa8N58y3Ltrr_-QTQ",  # Make sure you have the correct token
        'Content-Type': 'application/json',
        }

        # Send a request to Power Automate
        payload = {
            "region": data['region'],
            "site": data['site'],
            "folder": data['folder'],
            "image_name": data['image_name'],
            "image_path": data['image_path']  # This should be the URL of the image
        }

        try:
            print("Sending payload to Power Automate:", payload)
            response = requests.post(power_automate_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            print("Power Automate response:", response.json())
        except requests.RequestException as e:
            print("Error sending to Power Automate:", e)
            if e.response is not None:
                print("Response content:", e.response.text)
