from django.urls import path
from . import views

urlpatterns = [
    path('send_friend_request/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:request_id>/', views.decline_friend_request, name='decline_friend_request'),
    path('notifications/', views.notifications, name='notifications'),
]