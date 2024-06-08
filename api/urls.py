from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
# router = DefaultRouter()
# router.register("")

urlpatterns = [
    path('download-instagram-post/<str:url>/', Instagram_Downloader.as_view(), name='download_instagram_post'),
    # path('proxy/', ProxyView, name='proxy-view'),
    path('get-profile-info/<str:username>/',GetProfileInfo.as_view(),name='get-profile-info'),
    path("get-story/<str:usrname>/<str:id>/",GetStory.as_view()),
]
