from django.contrib import admin
from groups.models import Tag, Group, GroupMembership
# Register your models here.

admin.site.register(Tag)
admin.site.register(Group)
admin.site.register(GroupMembership)
