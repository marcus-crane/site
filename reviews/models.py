import datetime

import CommonMark
from django.db import models
from django.utils.text import slugify

class Review(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=40, blank=True, unique=True)
	text = models.TextField()
	date = models.DateField(
			'Publication date',
			blank=True, null=True)
	cover = models.URLField()
	backdrop = models.URLField()

	def save(self, *args, **kwargs):
		"""
		When saving, automatically generate a slug from the title
		"""
		self.slug = slugify(self.title)
		super(Review, self).save(*args, **kwargs)

	def render(self):
		return CommonMark.commonmark(self.text)

	def __str__(self):
		return self.title