from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# import instaloader

from .models import *

class InstagramPostDownload(APIView):
    def get(self,request):
        for i in range(5):
            UploadMedia.objects.create(name = "raja")
        return Response({"status":"success"})

        #  UploadMedia.objects.create(name = "raja")