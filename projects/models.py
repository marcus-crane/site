import CommonMarkExtensions.tables
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Project(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=40, blank=True, unique=True)
  date = models.DateField(blank=False)
  summary = models.CharField(max_length=140)
  text = models.TextField()

  def save(self, *args, **kwargs):
    """
    When saving, automatically generate the slug from the title
    """
    self.slug = slugify(self.title)
    super(Project, self).save(*args, **kwargs)

  def render(self):
    """
    Render post markdown to HTML with code highlighting support.
    """
    return CommonMarkExtensions.tables.commonmark(self.text)

  def __str__(self):
    return self.title