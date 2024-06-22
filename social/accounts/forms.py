from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate, get_user_model

Users = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = Users  # Используйте вашу модель Users
        fields = ['username','email', 'password1', 'password2']  # Удалите 'username'

class UserLoginForm(forms.Form):
    username_or_email = forms.CharField(label='Имя пользователя или email', widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя или email', 'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username_or_email, password=password)
        if not user:
            raise forms.ValidationError('Неверные учетные данные')
        return self.cleaned_data
    
class EditProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2025))
    )
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'birth_date', 'bio', 'photo']