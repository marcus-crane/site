from django.db import models

class Episode(models.Model):
    show = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    watched = models.DateTimeField()
    season = models.IntegerField()
    number = models.IntegerField()
    tmdb = models.IntegerField()
    cover = models.URLField()
    url = models.URLField()

    def __str__(self):
        return '{}x{} {}'.format(self.season, self.number, self.name)

class Movie(models.Model):
    name = models.CharField(max_length=200)
    watched = models.DateTimeField()
    tmdb = models.IntegerField()
    cover = models.URLField()
    url = models.URLField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.year)