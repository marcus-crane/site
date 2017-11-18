from django.utils import timezone
from django.views import generic

from .models import Post

class PostView(generic.ListView):
  template_name = 'blog/list.html'
  context_object_name = 'posts'

  def get_queryset(self):
    """ Fetch only published posts, and order by descending date """
    return Post.objects.filter(date__lte=timezone.now(), status="P").order_by('-date')

class PostDetailView(generic.DetailView):
  model = Post
  queryset = Post.objects.exclude(status='D')
  template_name = 'blog/detail.html'