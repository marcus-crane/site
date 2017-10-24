from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40)
    text = models.TextField()
    created_date = models.DateTimeField(
            'Creation date',
            default=timezone.now)
    published_date = models.DateTimeField(
            'Publication date',
            blank=True, null=True)
    draft = models.BooleanField(
            'Draft post?',
            default=True)

    def publish(self):
        self.draft = False
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
