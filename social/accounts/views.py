from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegisterForm, UserLoginForm, EditProfileForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.mail import send_mail
from django.conf import settings
from accounts.utils import send_verification_email
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator

User = get_user_model()


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user, request)
            return render(request, 'register/registration_success.html') 
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
    section = request.GET.get('section', 'my_posts')
    my_posts = user.get_my_posts()
    saved_posts = user.get_saved_posts()
    liked_posts = user.get_liked_posts()
    return render(request, 'accounts/profile.html', {
        'user': user,
        'section': section,
        'my_posts': my_posts,
        'saved_posts': saved_posts,
        'liked_posts': liked_posts
    })

def logout_view(request):
    logout(request)
    return redirect('login')

def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    user.is_verified = True
    user.save()
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form':form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user ,request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form':form})


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        section = 'my_posts'
        my_posts = user.get_my_posts()
        return render(request, 'accounts/user_profile.html', {
            'user': user,
            'section': section,
            'my_posts': my_posts
        })
    

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'password/password_reset_form.html'
    email_template_name = 'password/password_reset_email.html'
    subject_template_name = 'password/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


# Представление для страницы подтверждения отправки инструкций по сбросу пароля
class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'


# Представление для установки нового пароля
class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


# Представление для страницы успешного сброса пароля
class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password/password_reset_complete.html'

