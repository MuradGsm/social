from django import forms
from public.models import Post,Hashtag

class PostForm(forms.ModelForm):
    hashtags = forms.CharField(max_length=200, help_text="Введите хэштеги через запятую")

    class Meta:
        model = Post
        fields = ['text', 'image', 'hashtags']