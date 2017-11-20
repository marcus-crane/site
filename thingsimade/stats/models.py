from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    cover = models.URLField()
    playcount = models.IntegerField()
    url = models.URLField()

class Episode(models.Model):
    show = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    watched = models.DateTimeField()
    season = models.IntegerField()
    number = models.IntegerField()
    tmdb = models.IntegerField()
    cover = models.URLField()

class Game(models.Model):
    steam_id = models.IntegerField()
    name = models.CharField(max_length=200)
    banner = models.URLField()
    playtime = models.IntegerField()
