from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from public.models import Post

class Users(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, default='img/default.png')
    is_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.username

    def get_my_posts(self):
        return self.posts.all()

    def get_saved_posts(self):
        return self.saved_posts.all()

    def get_liked_posts(self):
        return Post.objects.filter(likes__user=self)