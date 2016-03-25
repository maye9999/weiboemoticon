from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OAuthUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    access_token = models.TextField(max_length=100)
    expire_time = models.IntegerField(default=0)