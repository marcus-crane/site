from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Post

def post_list(request):
    posts = Post.objects.filter(
                date__lte=timezone.now()
            ).order_by('-date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})