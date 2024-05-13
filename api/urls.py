from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import InstagramPostDownload
# router = DefaultRouter()
# router.register("")

urlpatterns = [
    path('download-instagram-post/', InstagramPostDownload.as_view(), name='download_instagram_post'),
]
