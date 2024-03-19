from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout

from weatherapp.models import CustomUser
from weatherapp.serializers import CustomUserSerializer
from .util import *


@permission_classes([AllowAny])
class Weather(APIView):
    def get(self, request, place):
        r = requests.get('https://api.openweathermap.org/data/2.5/weather', 
                         params={
                             'appid': '29ba9d6026a20f23cbac7efefc77d6f2', 
                             'q': place,
                         })
        
        weatherdata = {
            "lon": r.json()["coord"]["lon"],
            "lat": r.json()["coord"]["lat"],
            "main": r.json()["weather"][0]["main"],
            "description": r.json()["weather"][0]["description"],
            "temp": r.json()["main"]["temp"]
        }
        
        a = requests.get('https://api.geoapify.com/v2/places',
                         params={
                             'apiKey': '48f592a34b3c493383f0aa8a2579489e',
                             'limit': 20,
                             'filter': f'circle:{weatherdata["lon"]},{weatherdata["lat"]},5000',
                             'categories': 'activity,catering,entertainment,leisure'
                         })
        
        data = {
            'place_name': r.json()['name'],
            'weather_data': weatherdata,
            'recommendation': recommend_activity(r.json()["weather"][0]["main"]),
            'activity_data': activity_data(a.json()),
        }
        return Response(data, status=status.HTTP_200_OK)
 
@permission_classes([AllowAny])
class User(APIView):
    def get(self, request):
        username = request.data.get('username')
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                serializer = CustomUserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'Username parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            serializer = CustomUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        username = request.data.get('username')
        try:
            user = CustomUser.objects.get(username=username)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
@permission_classes([AllowAny])
class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if username:
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        elif email:
            if validate_email(email):
                user = authenticate(request, email=email, password=password)
                if user:
                    login(request, user)
                    return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message': 'Invalid email format'}, status=status.HTTP_400_BAD_REQUEST)
       
        else:
            return Response({'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
class Logout(APIView):
    def get(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

