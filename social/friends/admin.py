from django.contrib import admin
from friends.models import FriendRequest, Friendship, Notification


# Register your models here.
admin.site.register(Friendship)
admin.site.register(FriendRequest)
admin.site.register(Notification)
