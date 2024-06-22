from django.urls import path
from .views import login_view, sign_up, verify_email, profile, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', sign_up, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/',logout_view, name='logout'),

    path('verify/<str:token>/', verify_email, name='verify_email'),
]
