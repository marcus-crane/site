from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from markdown2 import markdown

class Project(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=40, blank=True)
  date = models.DateField(blank=False)
  text = models.TextField()

  def save(self, *args, **kwargs):
    """
    When saving, automatically generate the slug from the title
    """
    self.slug = slugify(self.title)
    super(Project, self).save(*args, **kwargs)

  def __str__(self):
    return self.title