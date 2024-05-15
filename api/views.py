from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *

import instaloader

class Instagram_Downloader(APIView):


    def get(self,request,url):
        try:
            my_Url = url
            loader = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(loader.context, my_Url)
            url_list = []
            if post._full_metadata['is_video']:
                try :

                    x = post._full_metadata['edge_sidecar_to_children']["edges"]
                except:
                    url_list.extend([{"video_c5_img_cover1":post._full_metadata['display_url']}])
                    url_list.extend([{"video_c5_1":post._full_metadata['video_url']}])

                    

                else:
                    for i in range(len(x)):
                        if x[i]["node"]['is_video'] :
                            url_list.extend([{f'video_c5_img_cover{i}':x[i]["node"]["display_resources"][0]["src"]}])
                            url_list.extend([{f'video_c5_{i}':x[i]["node"]["video_url"]}])
                            continue
                        url_list.extend([{f'img_c5_{i}':x[i]["node"]["display_resources"][0]["src"]}])
            else:
                try :

                    x = post._full_metadata['edge_sidecar_to_children']["edges"]
                except:
                    url_list.extend([{"img_c5_1":post._full_metadata['display_url']}])
                else:
                    
                    for i in range(len(x)):
                        if x[i]["node"]['is_video'] :
                            url_list.extend([{f'video_c5_img_cover{i}':x[i]["node"]["display_resources"][0]["src"]}])
                            url_list.extend([{f'video_c5_{i}':x[i]["node"]["video_url"]}])
                            continue
                        url_list.extend([{f'img_c5_{i}':x[i]["node"]["display_resources"][0]["src"]}])
            
            return Response(url_list)

        except:
            return Response({"status":"faild"})

    
    