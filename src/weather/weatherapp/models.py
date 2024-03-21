import uuid
from django.db import models

class CustomUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    tags = models.TextField()

class RecommendationChoice(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

class UserChoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chosen_city = models.CharField(max_length=25)
    recommendations = models.ManyToManyField(RecommendationChoice)
    weather = models.CharField(max_length=25)
