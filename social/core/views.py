from django.shortcuts import render, redirect
from public.models import Post, Hashtag, Like
from public.forms import PostForm

def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            hashtags = form.cleaned_data['hashtags'].split(',')
            for tag in hashtags:
                tag = tag.strip()
                if tag:
                    hashtag, created = Hashtag.objects.get_or_create(name=tag)
                    post.hashtags.add(hashtag)
            return redirect('home')
    else:
        form = PostForm()
    
    posts = Post.objects.all().order_by('-created_at')
    liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True) if request.user.is_authenticated else []
    return render(request, 'core/home.html', {'posts': posts, 'form': form, 'liked_posts': liked_posts})