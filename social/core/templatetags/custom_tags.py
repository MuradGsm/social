from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()

@register.simple_tag
def get_all_users_except_current(current_user):
    return User.objects.exclude(id=current_user.id).order_by('-date_joined')