from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
    # path('upload/', views.upload_image, name='upload_image'),
    # path('upload/', views.UploadImageView.as_view(), name='upload_image'),
    path('upload/', views.upload_to_sharepoint, name='upload_image'),
]
