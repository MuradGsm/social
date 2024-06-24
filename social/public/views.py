from django.shortcuts import render, get_object_or_404, redirect
from public.models import Post, Like, Comment, SavedPost
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'like_count': post.like_count()})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(author=request.user, post=post, text=text)
    return redirect('home')

def save_post(request, post_id):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
        if created:
            message = 'Пост успешно сохранен.'
        else:
            message = 'Пост уже сохранен.'
        return JsonResponse({'message': message})
    return JsonResponse({'message': 'Неверный запрос.'}, status=400)