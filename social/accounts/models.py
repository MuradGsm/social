from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, default='img/default.png')
    is_verified = models.BooleanField(default=False)  # Добавь это поле для отслеживания верификации
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username