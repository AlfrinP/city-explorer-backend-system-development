from django.contrib import admin
from django.urls import path
from weatherapp.views import *

urlpatterns = [
    path('admin', admin.site.urls),
    path('weather/<str:place>/', Weather.as_view()),
    path('user', User.as_view()),
    path('login',Login.as_view(), name='login'),
    path('logout',Logout.as_view() , name='logout'),
]
