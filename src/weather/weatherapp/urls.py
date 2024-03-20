from django.contrib import admin
from django.urls import path
from weatherapp.views import *

urlpatterns = [
    path('admin', admin.site.urls),
    path('weather/<str:place>/', Weather.as_view()),
    path('user', User.as_view()),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('register/', RegistrationAPIView.as_view(), name='user-registration'),
    path('refresh/', RefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', LogoutAPIView.as_view(), name="user-logout")
    # path('tags',Preferences.as_view() , name='logout'),
]
