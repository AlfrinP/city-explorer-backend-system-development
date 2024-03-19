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
    chosen_city = models.CharField(max_length=25,default=None)
    chosen_activity = models.CharField(max_length=25,default=None)
    weather = models.CharField(max_length=25)