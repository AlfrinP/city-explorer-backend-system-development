from rest_framework import serializers
from .models import CustomUser, UserProfile, UserChoice, RecommendationChoice
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'tags']

class RecommendationChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationChoice
        fields = ['name', 'district', 'street', 'address', 'phone']

class UserChoiceSerializer(serializers.ModelSerializer):
    recommendations = RecommendationChoiceSerializer()  # Serialize nested RecommendationChoice
    class Meta:
        model = UserChoice
        fields = ['user', 'chosen_city', 'recommendations', 'weather']
