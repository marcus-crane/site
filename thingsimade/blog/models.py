from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from markdown2 import markdown

class Post(models.Model):
    POST_STATUS = (
        ('D', 'Draft'),
        ('U', 'Unlisted'),
        ('P', 'Published'),
    )
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, blank=True)
    text = models.TextField()
    date = models.DateTimeField(
            'Publication date',
            blank=True, null=True)
    status = models.CharField(max_length=1,
        choices=POST_STATUS)

    def save(self, *args, **kwargs):
        """
        When saving, automatically generate the slug from the title
        """
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def render(self):
        """
        Render post markdown to HTML with code highlighting support.
        """
        return markdown(self.text, extras=['fenced-code-blocks'])

    def prev(self):
        """
        Return the id of the previous post
        """
        try:
            return Post.objects.get(id=self.id - 1).slug
        except:
            return None

    def next(self):
        """
        Return the id of the next post
        """
        #return Post.objects.get(id=self.id + 1).slug
        try:
            return Post.objects.get(id=self.id + 1).slug
        except:
            return None

    def pull_excerpt(self):
        """
        Pull the first paragraph of a post to use in the post list
        """
        return self.text.split('\n')[0]

    def publish(self):
        """
        Publish a post which sets a date making it publically visible
        """
        self.status = 'P'
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
