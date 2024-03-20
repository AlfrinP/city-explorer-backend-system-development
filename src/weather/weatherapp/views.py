from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

import requests

from weatherapp.authenticate import *
from weatherapp.models import *
from weatherapp.serializers import *
from weatherapp.util import *
from weatherapp.validate import *


from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password



class Weather(APIView):
    def get(self, request):
        place = request.POST.get('city')
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        if id:
            if validate_city(place):
                r = requests.get('https://api.openweathermap.org/data/2.5/weather',
                                 params={
                                     'appid': '29ba9d6026a20f23cbac7efefc77d6f2',
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

                    description, category = recommend_activity(
                        r.json()["weather"][0]["main"])
                    print("Description:", description)
                    print("Category:", category)

                    a = requests.get('https://api.geoapify.com/v2/places',
                                     params={
                                         'apiKey': '48f592a34b3c493383f0aa8a2579489e',
                                         'limit': 20,
                                         'filter': f'circle:{weatherdata["lon"]},{weatherdata["lat"]},5000',
                                         'categories': category,
                                     })

                    if a.status_code == 200:
                        data = {
                            'place_name': r.json()['name'],
                            'weather_data': weatherdata,
                            'recommendation': description,
                            'category': category,
                            'activity_data': activity_data(a.json()),
                        }
                        userhistory_serializer = UserChoiceSerializer(data={'chosen_city': place, 'chosen_activity': activity_data(a.json()), 'weather': r.json()["weather"][0]["main"]})

                        if userhistory_serializer.is_valid():
                            userhistory_serializer.save()
                            return Response(data, status=status.HTTP_200_OK)
                        else:
                            return Response(userhistory_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({'message': 'Failed to fetch activity data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
        if id:
            try:
                user = CustomUser.objects.get(id=id)
                data={
                   "user_data":CustomUserSerializer(user).data,
                   "preferences":UserProfileSerializer(user).data,
                   "history":UserChoiceSerializer(user).data,
                }
                return Response(data, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User is no logged in !'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user_serializer = CustomUserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            tags = request.data.get('tags', [])
            if tags:
                user_profile, _ = UserProfile.objects.get_or_create(user=user)
                user_profile.tags = tags
                user_profile.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        refresh_token = request.COOKIES.get('refreshToken')
        id = decode_refresh_token(refresh_token)
        try:
            user = CustomUser.objects.get(id=id)
            serializer = CustomUserSerializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User updated successfully', 'user': serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
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
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        EoM = data.get('EmailOrUsername')
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
