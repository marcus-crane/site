from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    link = models.URLField()
    author = models.CharField(max_length=200)

    def __str__(self):
        return "{0} by {1}".format(self.name, self.author)

class Game(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    link = models.URLField()
    year = models.IntegerField()
    platform = models.CharField(max_length=200)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.year)

class Movie(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    link = models.URLField()
    year = models.IntegerField()

    def __str__(self):
        return "{0} ({1})".format(self.name, self.year)

class Song(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    link = models.URLField()
    artist = models.CharField(max_length=200)

    def __str__(self):
        return "{0} - {1}".format(self.name, self.artist)

class Show(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField()
    link = models.URLField()
    series = models.CharField(max_length=200)

    def __str__(self):
        return "{0} - {1}".format(self.name, self.series)