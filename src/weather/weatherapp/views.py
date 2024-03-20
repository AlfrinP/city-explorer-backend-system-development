from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from weatherapp.authenticate import *
from weatherapp.models import *
from weatherapp.serializers import *
from weatherapp.util import *
from weatherapp.validate import *


from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

import requests

import os
from dotenv import load_dotenv
load_dotenv()


WEATHER_KEY = os.getenv('WEATHER_KEY'),
GEOAPIFY_KEY = os.getenv('GEOAPIFY_KEY')


class Weather(APIView):
    def get(self, request):
        place = request.data.get('city')
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        if CustomUser.objects.filter(id=id).exists():
            user = CustomUser.objects.get(id=id)
            if validate_city(place):
                r = requests.get('https://api.openweathermap.org/data/2.5/weather',
                                 params={
                                     'appid': WEATHER_KEY,
                                     'q': place,
                                 })

                if r.status_code == 200:
                    weatherdata = {
                        "lon": r.json()["coord"]["lon"],
                        "lat": r.json()["coord"]["lat"],
                        "main": r.json()["weather"][0]["main"],
                        "description": r.json()["weather"][0]["description"],
                        "temp": r.json()["main"]["temp"]
                    }
                    descriptions, categories = recommend_activity(
                        r.json()["weather"][0]["main"])
                    activity_data_list = []
                    a = requests.get('https://api.geoapify.com/v2/places?',
                                     params={
                                         'apiKey': GEOAPIFY_KEY,
                                         'limit': 10,
                                         'filter': f'circle:{weatherdata["lon"]},{weatherdata["lat"]},5000',
                                         'categories': categories,
                                     })
                    if a.status_code == 200:
                        activity_data_list.extend(activity_data(a.json()))
                        recommendation, _ = RecommendationChoice.objects.get_or_create(
                            name=descriptions,
                            defaults={'district': '', 'street': '',
                                        'address': '', 'phone': ''}
                        )
                        if not UserChoice.objects.filter(user=user,
                                                            chosen_city=place,
                                                            weather=weatherdata["main"]).exists():
                            UserChoice.objects.create(
                                user=user,
                                chosen_city=place,
                                recommendations=recommendation,
                                weather=weatherdata["main"]
                            )
                    else:
                        return Response({'message': 'Failed to fetch activity data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                    data = {
                        'place_name': r.json()['name'],
                        'weather_data': weatherdata,
                        'recommendations': descriptions,
                        'category': categories,
                        'activity_data': activity_data_list,
                    }

                    return Response(data, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Failed to fetch weather data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'message': 'City name should only contain alphabets!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'User is not logged in!'}, status=status.HTTP_400_BAD_REQUEST)
        
class User(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        print(id)
        if CustomUser.objects.filter(id=id).exists():
            try:
                user = CustomUser.objects.get(id=id)
                return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User is no logged in !'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        if CustomUser.objects.filter(id=id).exists():
            user = CustomUser.objects.get(id=id)
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'User not logged in !'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        try:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not logged in !'}, status=status.HTTP_404_NOT_FOUND)


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        access_token = create_access_token(id)
        return Response({
            'token': access_token
        })


class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="refreshToken")
        response.data = {
            'message': "SUCCESS"
        }
        return response


class RegistrationAPIView(APIView):
    def post(self, request):
        data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'email': request.data.get('email'),
        }
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            tag_serializer = UserProfileSerializer()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        EoM = data.get('emailorusername')
        print(EoM)
        if EoM is None:
            raise APIException('EmailOrUsername is a mandatory field.')
        try:
            user = CustomUser.objects.get(username=EoM)
        except ObjectDoesNotExist:
            user = None
        if user is None:
            try:
                user = CustomUser.objects.get(email=EoM)
            except ObjectDoesNotExist:
                user = None
        print(user)
        if user is None:
            raise APIException('Invalid Credentials')

        if not user or not check_password(request.data['password'], user.password):
            raise APIException('Invalid Credentials')

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        response = Response()

        response.set_cookie(key='refreshToken',
                            value=refresh_token, httponly=True)
        response.data = {
            'access-token': access_token,
            'refresh-token': refresh_token
        }

        return response


class Preference(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        try:
            user = CustomUser.objects.get(id=id)
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            existing_tags = user_profile.tags.split(
                ',') if user_profile.tags else []
            return Response({'tags': existing_tags}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not logged in !'}, status=status.HTTP_404)

    def post(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        try:
            user = CustomUser.objects.get(id=id)
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            user_serializer = CustomUserSerializer(
                user,
                data={'username': user.username, "password": user.password},
                partial=True
            )
            if user_serializer.is_valid():
                existing_tags = user_profile.tags.split(',') if user_profile.tags else []
                new_tags_str = request.data.get('tags', '')
                new_tags = new_tags_str.split(',')
                updated_tags = existing_tags + new_tags
                updated_tags_str = ','.join(updated_tags)
                user_profile.tags = updated_tags_str
                user_profile.save()

                return Response({
                    'message': 'User updated successfully',
                    'user': user_serializer.data,
                    'tags': updated_tags
                }, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not logged in !'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        try:
            user = CustomUser.objects.get(id=id)
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            tag_to_delete = request.data.get('tag', '')
            existing_tags = user_profile.tags.split(
                ',') if user_profile.tags else []
            if tag_to_delete in existing_tags:
                existing_tags.remove(tag_to_delete)
                updated_tags_str = ','.join(existing_tags)
                user_profile.tags = updated_tags_str
                user_profile.save()

                return Response({'message': 'Tag deleted successfully', 'tags': existing_tags}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Tag not found'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not logged in !'}, status=status.HTTP_404)

class History(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        try:
            user = CustomUser.objects.get(id=id) 
            print(user)
            user_choices_data = UserChoiceSerializer(user)
            return Response(user_choices_data.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not logged in!'}, status=status.HTTP_404_NOT_FOUND)