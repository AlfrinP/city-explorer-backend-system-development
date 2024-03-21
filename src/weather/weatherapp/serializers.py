from rest_framework import serializers
from .models import CustomUser, UserProfile, UserChoice, RecommendationChoice

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'tags']

class RecommendationChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationChoice
        fields = ['name', 'city', 'street', 'address', 'phone']

class UserChoiceSerializer(serializers.ModelSerializer):
    recommendations = RecommendationChoiceSerializer(many=True)
    class Meta:
        model = UserChoice
        fields = ['user', 'chosen_city', 'recommendations', 'weather']
