from django.urls import path
from public import views

urlpatterns = [
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
]