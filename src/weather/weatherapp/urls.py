from django.contrib import admin
from django.urls import path
from weatherapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('weather/', Weather.as_view(), name='weather'),
    path('user/', User.as_view(), name='user'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout"),
    path('tags/', Preference.as_view(), name='user-preference'),
    path('history/', History.as_view(), name='user-history'),
]
