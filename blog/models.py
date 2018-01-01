import datetime

import CommonMarkExtensions.tables
from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    POST_STATUS = (
        ('D', u'✍︎ Draft'),
        ('U', u'⏏︎ Unlisted'),
        ('P', u'✔ Published'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=40, blank=True, unique=True)
    text = models.TextField()
    head = models.TextField(blank=True)
    foot = models.TextField(blank=True)
    date = models.DateField(
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

    def publish(self):
        """
        Convert a draft or unlisted post to be visible right now
        """
        self.date = datetime.datetime.now()
        self.status = 'P'
        self.save()

    def render(self):
        """
        Render post markdown to HTML with code highlighting support.
        """
        return CommonMarkExtensions.tables.commonmark(self.text)

    def __str__(self):
        return self.title
