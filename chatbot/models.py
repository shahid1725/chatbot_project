
from django.db import models

class ItemImage(models.Model):
    technician_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    folder = models.CharField(max_length=255)
    image_path = models.CharField(max_length=255)
    upload_status = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
