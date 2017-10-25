from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from .models import Post

class PostView(generic.ListView):
  template_name = 'blog/post_list.html'
  context_object_name = 'posts'

  def get_queryset(self):
    """ Order posts by date in descending order."""
    return Post.objects.filter(date__lte=timezone.now()).order_by('-date')[:3]

class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'