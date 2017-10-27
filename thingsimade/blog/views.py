from django.utils import timezone
from django.views import generic

from .models import Post

class PostView(generic.ListView):
  template_name = 'blog/list.html'
  context_object_name = 'posts'

  def get_queryset(self):
    """ Order posts by date in descending order."""
    return Post.objects.filter(date__lte=timezone.now()).order_by('-date')

class PostDetailView(generic.DetailView):
  model = Post
  template_name = 'blog/detail.html'