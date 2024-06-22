from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegisterForm, UserLoginForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.conf import settings
from accounts.utils import send_verification_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


User = get_user_model()

# accounts/views.py

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user, request)
            return render(request, 'registration_success.html') 
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username_or_email, password=password)
            if user:
                if user.is_verified:
                    login(request, user)
                    return redirect('profile')
                else:
                    form.add_error(None, 'Пожалуйста, подтвердите свой email перед входом.')
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('login')

def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    user.is_verified = True
    user.save()
    return redirect('login')