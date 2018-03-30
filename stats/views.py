from django.shortcuts import render

from .models import Book, Movie, Song, Show

def stats(request):
    data = {
        'books': Book.objects.all(),
        'movies': Movie.objects.all()[:6],
        'music': Song.objects.all()[:6],
        'shows': Show.objects.all()[:6]
    }
    return render(request, 'stats/index.html', data)