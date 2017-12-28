from django.db import models

class Episodes(models.Model):
    show = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    watched = models.DateTimeField()
    season = models.IntegerField()
    number = models.IntegerField()
    tmdb = models.IntegerField()
    cover = models.URLField()

class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    watched = models.DateTimeField()
    tmdb = models.IntegerField()
    cover = models.URLField()
