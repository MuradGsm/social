from django import forms
from chats.models import Message

class MesasageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content',]