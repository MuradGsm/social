from django.urls import path
from groups import views

urlpatterns = [
    path('create/', views.cerate_group, name='create_group'), 
    path('', views.group_lis, name='group_list'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/manage', views.manage_group, name='manage_group'),
    path('<int:pk>/join', views.join_group, name='join_group'),
]