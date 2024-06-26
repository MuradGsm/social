from django import forms
from groups.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'category', 'tags', 'avatar']