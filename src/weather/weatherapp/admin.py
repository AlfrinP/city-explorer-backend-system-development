from django.contrib import admin
from .models import *

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserChoiceInline(admin.TabularInline):
    model = UserChoice


class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline, UserChoiceInline]

admin.site.register(CustomUser, CustomUserAdmin)
