# # image_transfer/models.py
# from django.db import models

# class ImageTransfer(models.Model):
#     image_url = models.URLField()
#     region = models.CharField(max_length=255)
#     site = models.CharField(max_length=255)
#     folder = models.CharField(max_length=255)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.region}/{self.site}/{self.folder}/image.jpg"


#-------------------------------------------------------------------------------



from django.db import models
from django.utils import timezone
import uuid

# class ImageUpload(models.Model):
#     image = models.ImageField(upload_to='temp_uploads/')
#     region = models.CharField(max_length=100)
#     site = models.CharField(max_length=100)
#     folder = models.CharField(max_length=100)
#     uploaded_at = models.DateTimeField(default=timezone.now)
#     processed = models.BooleanField(default=False)
#     sharepoint_url = models.URLField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.region}/{self.site}/{self.folder}/{self.image.name}"


class ImageTracking(models.Model):
    STATUS_CHOICES = [
        ('RECEIVED', 'Received from WhatsApp'),
        ('PROCESSING', 'Processing by Power Automate'),
        ('UPLOADED', 'Uploaded to SharePoint'),
        ('FAILED', 'Failed'),
    ]

    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False)
    whatsapp_message_id = models.CharField(max_length=100, null=True, blank=True)
    image_name = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    folder = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    power_automate_flow_id = models.CharField(max_length=100, null=True, blank=True)
    sharepoint_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.tracking_id} - {self.status}"



#----------------------------------------------------------------------------------

class ImageUpload(models.Model):
    region = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    folder = models.CharField(max_length=100)
    image_name = models.CharField(max_length=255,null=True,blank=True)
    image_path = models.CharField(max_length=255,null=True,blank=True)  # URL to the uploaded image
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image_name