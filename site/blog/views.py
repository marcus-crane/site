import datetime
from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.urls import reverse
from django.views import generic

from .models import Post

class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.exclude(status='D')
    template_name = 'blog/detail.html'

class PostView(generic.ListView):
    template_name = 'blog/list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """ Fetch only published posts, and order by descending date """
        return Post.objects.filter(
            published_at__lte=timezone.now(), status="P"
        ).order_by('-published_at')

class RSSFeed(Feed):
    title = "utf9k"
    link = "/blog/"
    description = "Blog posts from utf9k"

    def items(self):
        return Post.objects.order_by('-published_at')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return datetime.datetime.combine(item.published_at, datetime.time())

    def item_description(self, item):
        return item.render()

    def item_link(self, item):
        return reverse('blog:detail', args=[item.slug])