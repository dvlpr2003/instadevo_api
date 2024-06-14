import base64
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
import requests
import os
import instaloader

class Instagram_Downloader(APIView):


    def get(self,request,url):
        try:
            my_Url = url
            print(my_Url)
            loader = instaloader.Instaloader()
            post = instaloader.Post.from_shortcode(loader.context, my_Url)
            print(post)
            url_list = []
            if post._full_metadata['is_video']:
                try :

                    x = post._full_metadata['edge_sidecar_to_children']["edges"]
                except:
                    img_response = requests.get(post._full_metadata['display_url'])
                    if img_response.status_code == 200:
                        image_binary = img_response.content
                        base64_image = base64.b64encode(image_binary).decode('utf-8')
                        img_data_url = f"data:image/jpeg;base64,{base64_image}"
                        rl = {
                            'url':{
                                "video" : True,
                                "video_img":img_data_url,
                                'video_c5':post._full_metadata['video_url'],
                                
                            }
                        }
                        url_list.append(rl)
                        return Response(url_list)
                    else:
                        return Response({'error': 'Failed to fetch Instagram media'})
                else:
                    rl_clone = []
                    for i in range(len(x)):
                        if x[i]["node"]['is_video'] :
                            img_response = requests.get(x[i]["node"]["display_resources"][0]["src"])
                            if img_response.status_code == 200:
                                image_binary = img_response.content
                                base64_image = base64.b64encode(image_binary).decode('utf-8')
                                img_data_url = f"data:image/jpeg;base64,{base64_image}"
                            rl = {
                                'url':{
                                    "video":True,
                                    f'video_img':img_data_url,
                                    f'video_c5':x[i]["node"]["video_url"],
                                }
                            }
                            rl_clone.append(rl)
                            
                            continue
                        img_response = requests.get(x[i]["node"]["display_resources"][0]["src"])
                        if img_response.status_code == 200:
                                image_binary = img_response.content
                                base64_image = base64.b64encode(image_binary).decode('utf-8')
                                img_data_url = f"data:image/jpeg;base64,{base64_image}"
                                rl = {
                                    'url':{
                                        'video':False,
                                        f'img_c5':img_data_url
                                    }
                                }
                                rl_clone.append(rl)
                    url_list.extend(rl_clone)
                    return Response(url_list)
            else:
                try :
                    x = post._full_metadata['edge_sidecar_to_children']["edges"]
                except:
                    img_response = requests.get(post._full_metadata['display_url'])
                    if img_response.status_code == 200:
                                
                                image_binary = img_response.content
                                base64_image = base64.b64encode(image_binary).decode('utf-8')
                                img_data_url = f"data:image/jpeg;base64,{base64_image}"
                                rl = {
                                    'url':{
                                         'video':False,
                                        f'img_c5':img_data_url
                                    }
                                }
                                url_list.append(rl)
                    else:
                        return Response({'error': 'Failed to fetch Instagram media'})
                    return Response(url_list)
                         



                else:
                    rl_clone = []
                    for i in range(len(x)):
                        if x[i]["node"]['is_video'] :
                            img_response = requests.get(x[i]["node"]["display_resources"][0]["src"])
                            if img_response.status_code == 200:

                            
                                image_binary = img_response.content
                                base64_image = base64.b64encode(image_binary).decode('utf-8')
                                img_data_url = f"data:image/jpeg;base64,{base64_image}"
                            # url_list.extend([{f'video_c5_img_cover{i}':x[i]["node"]["display_resources"][0]["src"]}])
                            # url_list.extend([{f'video_c5_{i}':x[i]["node"]["video_url"]}])
                            rl = {
                                'url':{
                                    "video":True,
                                    f'video_img':img_data_url,
                                    f'video_c5':x[i]["node"]["video_url"],
                                }
                            }
                            rl_clone.append(rl)
                            
                            continue
                        # url_list.extend([{f'img_c5_{i}':x[i]["node"]["display_resources"][0]["src"]}])
                        img_response = requests.get(x[i]["node"]["display_resources"][0]["src"])
                        if img_response.status_code == 200:
                                image_binary = img_response.content
                                base64_image = base64.b64encode(image_binary).decode('utf-8')
                                img_data_url = f"data:image/jpeg;base64,{base64_image}"
                                rl = {
                                    'url':{
                                         'video':False,
                                        f'img_c5':img_data_url
                                    }
                                }
                                rl_clone.append(rl)
                    url_list.extend(rl_clone)
                    return Response(url_list)
            
            # return Response(url_list)
        
        

        except:
            return Response({"status":"faild"})

from instaloader.exceptions import ProfileNotExistsException, ConnectionException, BadResponseException, LoginRequiredException
class GetProfileInfo(APIView):
     
     def get(self,request,username):
            
            loader = instaloader.Instaloader()
            # os.system("rm -f ~/.config/instaloader/session-krishna_.kumar_.054")
            userid = os.getenv('INSTAGRAM_USER')
            password = os.getenv('INSTAGRAM_PASS')
            session_file = f"session-{userid}"
          
            try:

                loader.load_session_from_file('krishna_.kumar_.054',session_file)
        
            except :
                os.system("rm -f ~/.config/instaloader/session-krishna_.kumar_.054")
                loader.login(userid,password)
                loader.save_session_to_file(session_file)
           
            try:
                profile = instaloader.Profile.from_username(loader.context, username)
                img_response = requests.get(profile.profile_pic_url)
                if img_response.status_code == 200:
                    image_binary = img_response.content
                    base64_image = base64.b64encode(image_binary).decode('utf-8')
                    profile_pic_url = f"data:image/jpeg;base64,{base64_image}"
                my_lst = []
                profile = instaloader.Profile.from_username(loader.context, username)

                for i in loader.get_stories(userids=[profile.userid]): #get profile story
                    for j in range(len(i._node['items'])):
                        img_response = requests.get(i._node['items'][j]['display_url'])
                        if img_response.status_code == 200:
                            image_binary = img_response.content
                            base64_image = base64.b64encode(image_binary).decode('utf-8')
                            story_cover = f"data:image/jpeg;base64,{base64_image}"
                            try:
                                 
                                Story = {
                                        "story_cover":story_cover,
                                        "story_video":i._node['items'][j]['video_resources'][0]['src']
                                    }
                                my_lst.append(Story)
                            except:
                                Story = {
                                        "story_cover":story_cover,
                                        # "story_video":i._node['items'][j]['display_resources'][0]['src']
                                        "story_video":story_cover
                                    }
                                my_lst.append(Story)
                profile_details = {
                    'username': profile.username,
                    'full_name': profile.full_name,
                    'bio': profile.biography,
                    'followers': profile.followers,
                    'following': profile.followees,
                    'posts': profile.mediacount,
                    'profile_pic_url': profile_pic_url,
                    'story':my_lst
                }
                print(profile_details)
                
                return Response(profile_details)
            except ProfileNotExistsException:
                return Response({'status':f"Profile '{username}' does not exist."})
            except LoginRequiredException:
                return Response({'status':"Login required to access this profile."})
            except ConnectionException as e:
                return Response({'status':f"Connection error: {e}"})
            except BadResponseException as e:
                return Response({'status':f"Bad response error: {e}"})
            except Exception as e:
                return Response({'status':f"An error occurred: {e}"})



class GetStory(APIView):
     def get(self,request,usrname,id):
        loader = instaloader.Instaloader()
        userid = os.getenv('INSTAGRAM_USER')
        password = os.getenv('INSTAGRAM_PASS')
        session_file = f"session-{userid}"
          
        try:
            loader.load_session_from_file('krishna_.kumar_.054',session_file)
        except :
            os.system("rm -f ~/.config/instaloader/session-krishna_.kumar_.054")
            loader.login(userid,password)
            loader.save_session_to_file(session_file)
        try:
            my_lst = None
            profile = instaloader.Profile.from_username(loader.context, usrname)
            for i in loader.get_stories(userids=[profile.userid]):
                    for j in range(len(i._node["items"])):
                        if i._node['items'][j]['id'] == str(id):
                            img_response = requests.get(i._node['items'][j]['display_url'])
                            if img_response.status_code == 200:
                                image_binary = img_response.content
                                base64_image = base64.b64encode(image_binary).decode('utf-8')
                                story_cover = f"data:image/jpeg;base64,{base64_image}"


                                try:
                                    Story = {
                                        "story_cover":story_cover,
                                        "story_video":i._node['items'][j]['video_resources'][0]['src']
                                        }
                                    my_lst = Story
                                except:
                                    Story = {
                                            "story_cover":story_cover,
                                            "story_video":story_cover
                                        }
                                    my_lst = Story
            return Response(my_lst)
        except:
            return Response({"status":"error"})

