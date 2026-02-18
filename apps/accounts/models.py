
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_online = models.BooleanField(default=False)  # Add this here!
    department = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

