from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
# router = DefaultRouter()
# router.register("")

urlpatterns = [
    path('download-instagram-post/<str:url>/', Instagram_Downloader.as_view(), name='download_instagram_post'),
]
