from django.shortcuts import render, redirect

from .models import Book, Game, Movie, Song, Show
from stats import sources

def stats(request):
    data = {
        'books': Book.objects.all(),
        'games': Game.objects.all(),
        'movies': Movie.objects.all()[:6],
        'music': Song.objects.all()[:6],
        'shows': Show.objects.all()[:6]
    }
    return render(request, 'stats/index.html', data)

def update(request):
    sources.books()
    sources.games()
    sources.movies()
    sources.music()
    sources.shows()
    return redirect('/stats')