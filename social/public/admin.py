from django.contrib import admin
from public.models import Post, Hashtag, SavedPost,Like, Comment, View

admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(SavedPost)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(View)
