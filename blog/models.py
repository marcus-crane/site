from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, blank=True)
    text = models.TextField()
    date = models.DateTimeField(
            'Publication date',
            blank=True, null=True)
    draft = models.BooleanField(
            'Draft post?',
            default=True)

    # When saving, automatically generate the slug from the title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.draft = False
        self.date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
