from django.urls import path
from chats import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('<int:chat_id>/send/', views.send_message, name='send_message'),
    path('start_chat/<int:user_id>/', views.start_chat, name='start_chat'),
]