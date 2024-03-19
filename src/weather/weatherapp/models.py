from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.JSONField(default=list)

class UserChoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity_chosen = models.CharField(max_length=25)
    weather = models.CharField(max_length=25)


