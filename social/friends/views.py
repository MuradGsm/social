from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from friends.models import FriendRequest, Friendship, Notification
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        messages.error(request, 'Запрос в друзья уже отправлен.')
    else:
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        Notification.objects.create(user=to_user, message=f'{request.user.username} отправиль вам запрос в друзя')
        messages.success(request, 'Запрос в друзья отправлен.')
    return redirect('home')
    
@login_required
def accept_friend_request(request, request_id):
    friend_request =get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        Friendship.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
        friend_request.accepted = True
        friend_request.save()
        Notification.objects.create(user=friend_request.from_user, message=f'{request.user.username} принял ваш запрос в друзья')
        messages.success(request, 'Запрос в друзья принят.')
    return  redirect('home')


@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        friend_request.delete()
        Notification.objects.create(user=friend_request.from_user, message=f'{request.user.username} отклонил ваш запрос в друзья.')
        messages.success(request, 'Запрос в друзья отклонен.')
    return redirect('home')