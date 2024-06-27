from django import forms
from friends.models import FriendRequest

class FriendRequestForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = ['to_user']
