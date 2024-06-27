from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    @staticmethod
    def are_friends(user1, user2):
        return Friendship.objects.filter(user1=user1, user2=user2).exists() or Friendship.objects.filter(user1=user2, user2=user1).exists()

    def remove(self):
        Friendship.objects.filter(user1=self.user1, user2=self.user2).delete()
        Friendship.objects.filter(user1=self.user2, user2=self.user1).delete()



class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def accept(self):
        Friendship.objects.create(user1=self.from_user, user2=self.to_user)
        self.accepted = True
        self.save()
        Notification.objects.create(user=self.from_user, message=f'{self.to_user.username} принял ваш запрос в друзья', friend_request=self)
        Notification.objects.create(user=self.to_user, message=f'Вы приняли запрос в друзья от {self.from_user.username}', friend_request=self)
        self.delete()

    def decline(self):
        Notification.objects.create(user=self.from_user, message=f'{self.to_user.username} отклонил ваш запрос в друзья.', friend_request=self)
        self.delete()

    @staticmethod
    def send_request(from_user, to_user):
        if not FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            friend = FriendRequest.objects.create(from_user=from_user, to_user=to_user)
            Notification.objects.create(user=to_user, message=f'{from_user.username} отправил вам запрос в друзья', friend_request = friend)



class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    friend_request = models.ForeignKey(FriendRequest, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def mark_as_read(self):
        self.read = True
        self.save()