import datetime

import requests
import CommonMark
from django.db import models
from .tasks import fetch_review_art

class Review(models.Model):
	gbid = models.CharField(max_length=10, unique=True)
	title = models.CharField(max_length=200, blank=True, unique=True)
	slug = models.SlugField(max_length=40, blank=True, unique=True)
	developer = models.CharField(max_length=200, blank=True, unique=True)
	fresh = models.BooleanField(default=True)
	text = models.TextField()
	date = models.DateField(
			'Publication date',
			blank=True, null=True)
	backdrop = models.URLField(blank=True)

	def save(self, *args, **kwargs):
		"""
		When saving, automatically generate a slug from the title
		"""
		if self.fresh:
			self = fetch_review_art(self)
		super(Review, self).save(*args, **kwargs)

	def render(self):
		return CommonMark.commonmark(self.text)

	def __str__(self):
		return self.title