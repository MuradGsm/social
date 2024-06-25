from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import FriendRequest, Notification

User = get_user_model()

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if request.user == to_user:
        messages.error(request, 'Вы не можете отправить запрос в друзья самому себе.')
    elif FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists() or FriendRequest.objects.filter(from_user=to_user, to_user=request.user).exists():
        messages.error(request, 'Запрос в друзья уже отправлен.')
    else:
        with transaction.atomic():
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            Notification.objects.create(user=to_user, message=f'{request.user.username} отправил вам запрос в друзья')
        messages.success(request, 'Запрос в друзья отправлен.')
    return redirect('home')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        with transaction.atomic():
            friend_request.accept()
            messages.success(request, 'Запрос в друзья принят.')
    else:
        messages.error(request, 'Вы не можете принять этот запрос в друзья.')
    return redirect('home')

@login_required
def decline_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user == request.user:
        with transaction.atomic():
            friend_request.decline()
            messages.success(request, 'Запрос в друзья отклонен.')
    else:
        messages.error(request, 'Вы не можете отклонить этот запрос в друзья.')
    return redirect('home')

@login_required
def notifications(request):
    notifications = request.user.notifications.select_related('friend_request').order_by('-created_at').all()
    return render(request, 'friends/notifications.html', {'notifications': notifications})

