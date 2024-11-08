
from django.db import models

# class MediaFile(models.Model):
#     media_url = models.URLField(max_length=500)
#     filename = models.CharField(max_length=255)
#     content_type = models.CharField(max_length=100)
#     size = models.PositiveIntegerField()
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     file = models.FileField(upload_to='mms_images/', blank=True, null=True)  # Save actual file

#     def __str__(self):
#         return f"{self.filename} ({self.content_type})"



class MediaFile(models.Model):
    media_url = models.URLField(max_length=500, blank=True, null=True)  # Store image URL if you want to pass to Power Automate
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='mms_images/', blank=True, null=True)  # Save actual file
    region = models.CharField(max_length=100, blank=True, null=True)
    site = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.media_url and self.file:
            # Generate URL or path to the file
            self.media_url = self.file.url
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.filename} ({self.content_type})"
