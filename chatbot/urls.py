from django.urls import path
from . import views

urlpatterns = [
    # path('webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
    # path('upload/', views.upload_image, name='upload_image'),
    # path('upload/', views.UploadImageView.as_view(), name='upload_image'),
    # path('upload/', views.upload_to_sharepoint, name='upload_image'),
    # path('upload/', views.UploadImageView.as_view(), name='upload-image'),
    path('webhook1/', views.whatsapp_webhook1, name='whatsapp-webhook'),
    path('test/', views.test_connection, name='test-connection'),


    path('webhook/', views.whatsapp_webhook, name='whatsapp-webhook'),
    path('power-automate-callback/', views.power_automate_callback, name='power-automate-callback'),
    path('status/<uuid:tracking_id>/', views.check_status, name='check-status'),
    path('verify/<uuid:tracking_id>/', views.verify_sharepoint, name='verify-sharepoint'),

    path('upload-image/', views.UploadImageView.as_view(), name='upload-image'),
]

