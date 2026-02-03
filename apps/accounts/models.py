from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_online = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.username