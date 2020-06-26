from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class UserCreateView(APIView):
    pass


class UserActivationView(APIView):
    def get (self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + '/api/v1/auth/users/activation/'
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        content = result.json()
        return Response(result)
