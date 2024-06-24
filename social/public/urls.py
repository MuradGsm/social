from django.urls import path
from public import views

urlpatterns = [
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>', views.add_comment, name='add_comment'),
    path('save_post/<int:post_id>/', views.save_post, name='save_post'),
]