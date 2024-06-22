from django.shortcuts import render, get_object_or_404, redirect
from public.models import Post, Like
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'like_count': post.like_count()})