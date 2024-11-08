

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from twilio.rest import Client
import requests
import base64
from datetime import datetime
import os
import logging
from .models import MediaFile

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)






import logging
import json
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Set up logger
logger = logging.getLogger(__name__)

@csrf_exempt
def twilio_webhook(request):
    if request.method == 'POST':
        try:
            logger.debug("Received Twilio webhook POST data:")
            logger.debug(json.dumps(dict(request.POST), indent=2))

            num_media = int(request.POST.get('NumMedia', 0))
            body_text = request.POST.get('Body', '')  
            logger.debug(f"Number of media items: {num_media}")

            if num_media == 0:
                logger.error("No media files in request.")
                return JsonResponse({'status': 'failed', 'error': 'No media files in request'}, status=400)

            # Parse region and site from message body
            body_parts = body_text.split()
            if len(body_parts) < 2:
                logger.error("Insufficient metadata in message body for region and site.")
                return JsonResponse({'status': 'failed', 'error': 'Insufficient metadata in message body (region and site required)'}, status=400)

            region, site = body_parts[0], body_parts[1]
            media_files = []



            access_token = f"Bearer {settings.ACCESS_TOKEN}"

            if not access_token:
                logger.error("Access token missing in settings.")
                return JsonResponse({'status': 'failed', 'error': 'Access token missing in settings'}, status=500)


            for i in range(num_media):
                media_url = request.POST.get(f'MediaUrl{i}')
                content_type = request.POST.get(f'MediaContentType{i}')

                logger.debug(f"Processing media {i}: URL: {media_url}, Content Type: {content_type}")

                if media_url:
                    try:
                        media_response = requests.get(
                            media_url,
                            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        )
                        logger.debug(f"Media download status code: {media_response.status_code}")

                        if media_response.status_code == 200:
                            filename = os.path.basename(media_url)
                            media_file = MediaFile(
                                media_url=media_url,
                                filename=filename,
                                content_type=content_type,
                                size=len(media_response.content),
                                region=region,
                                site=site
                            )
                            media_file.save()
                            media_files.append(media_file)

                            # Pass access_token to Power Automate function

                            # power_automate_response = trigger_power_automate(media_file.media_url, region, site, access_token)
                            # if power_automate_response.get("status") != "success":
                            #     logger.error(f"Error triggering Power Automate for {filename}: {power_automate_response}")

                            send_image_to_sharepoint(media_file.id,access_token)



                        else:
                            logger.error(f"Failed to download media {i}. Status Code: {media_response.status_code}")
                    except Exception as e:
                        logger.error(f"Error downloading media {i}: {str(e)}")

            return JsonResponse({
                "status": "success",
                "message": f"Received {len(media_files)} media files",
                "media_files": [{'filename': mf.filename, 'status': 'stored'} for mf in media_files],
            }, status=200)

        except Exception as e:
            logger.error(f"Error in webhook: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": str(e),
                "debug_info": {
                    "post_data": dict(request.POST)
                }
            }, status=500)

    return JsonResponse({'status': 'failed', 'error': 'Invalid request method'}, status=405)


def send_image_to_sharepoint(media_file_id,access_token):
    try:
        # Retrieve the media file by ID
        media_file = MediaFile.objects.get(id=media_file_id)

        logger.debug(f"Access Token: {access_token}")
        
        # Prepare the data to send to Power Automate (HTTP Request)
        payload = {
            'region': media_file.region,
            'site': media_file.site,
            'image_url': media_file.media_url,
            'image_name': media_file.filename
        }

        headers = {
            # 'Authorization': f"Bearer {settings.ACCESS_TOKEN}", # If using OAuth
            'Content-Type': 'application/json'
        }

        # Send a POST request to Power Automate
        response = requests.post(settings.POWER_AUTOMATE_FLOW_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            logger.debug(f"Image {media_file.filename} sent to SharePoint successfully.")
            return JsonResponse({'status': 'success', 'message': 'Image sent to SharePoint successfully'})
        else:
            logger.error(f"Failed to send image to SharePoint. Status Code: {response.status_code}, Response: {response.text}")
            return JsonResponse({'status': 'error', 'message': 'Failed to send image to SharePoint'})
    except MediaFile.DoesNotExist:
        logger.error(f"MediaFile with ID {media_file_id} not found.")
        return JsonResponse({'status': 'error', 'message': 'Media file not found'})
    except Exception as e:
        logger.error(f"Error sending image to SharePoint: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})


