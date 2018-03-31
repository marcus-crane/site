from django.http import HttpResponse
from django.shortcuts import render

from .models import Book, Movie, Song, Show
from stats import sources

def stats(request):
    data = {
        'books': Book.objects.all(),
        'movies': Movie.objects.all()[:6],
        'music': Song.objects.all()[:6],
        'shows': Show.objects.all()[:6]
    }
    return render(request, 'stats/index.html', data)

def update(request):
    sources.books()
    sources.movies()
    sources.music()
    sources.shows()
    return HttpResponse('Updated!')