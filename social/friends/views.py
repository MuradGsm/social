from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from friends.models import FriendRequest, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def send_friend_request(request):
    if request.method == 'POST':
        to_user_id = request.POST.get('to_user')
        to_user = User.objects.get(id=to_user_id)
        FriendRequest.send_request(from_user=request.user, to_user=to_user)
        return redirect('user_profile', user_id=to_user_id)
    return redirect('home')


@login_required
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.accept()
    return redirect('home')

@login_required
def decline_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user:
        friend_request.decline()
    return redirect('home')

@login_required
def notifications(request):
    notifications = request.user.notifications.all()
    return render(request, 'friends/notifications.html', {'notifications': notifications})