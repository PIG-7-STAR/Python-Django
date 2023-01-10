from django.shortcuts import render
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login, authenticate


class Login(APIView):
    def post(self, request):
        User = get_user_model
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error" : "Please fill all fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check_user = User.objects.filter(username=username).exists()
        # if check_user == False:
        #     return Response({"error" : "Username does not exists"}, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # create token
            token, created = Token.objects.get_or_create(user=request.user)
            data = {
                'user_id': request.user.pk,
                'token': token.key,
                'username': request.user.username,
                'name': request.user.first_name + " " + request.user.last_name,
                'roles': request.user.roles
            }
            return Response({"success" : "Successfully login", "data": data }, status=status.HTTP_200_OK)
        else:
            return Response({"error" : "Invalid login detail"}, status=status.HTTP_400_BAD_REQUEST)