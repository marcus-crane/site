from django.conf import settings
from celery import shared_task

from .models import Episode
from .models import Movie

import maya
import requests

def query_trakt(endpoint):
    headers = { 'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': settings.TRAKT }
    url = 'https://api.trakt.tv/users/sentry/history/{}'.format(endpoint)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()

# Season and number are optional based on type
def fetch_cover(type, tmdb_id, season=None, number=None):
    if type == 'movie':
        url = ('https://api.themoviedb.org/3/movie/{}/images'
               '?api_key={}'.format(tmdb_id, settings.TMDB))
    if type == 'show':
        url = ('https://api.themoviedb.org/3/tv/{}/season/{}/episode/{}/images'
               '?api_key={}'.format(tmdb_id, season, number, settings.TMDB))
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if type == 'movie':
            img = data['posters'][0]['file_path']
        if type == 'show':
            img = data['stills'][0]['file_path']
        return 'https://image.tmdb.org/t/p/w780/{}'.format(img)

@shared_task
def fetch_shows():
    data = query_trakt('episodes')
    Episode.objects.all().delete()
    for entry in data:
        tmdb = entry['show']['ids']['tmdb']
        season = entry['episode']['season']
        number = entry['episode']['number']
        cover = fetch_cover('show', tmdb, season, number)
        Episode.objects.create(
            show=entry['show']['title'], name=entry['episode']['title'],
            watched=maya.parse(entry['watched_at']).datetime(),
            season=season, number=number, tmdb=tmdb, cover=cover,
            url = 'http://www.imdb.com/title/{}/'.format(entry['episode']['ids']['imdb']))

@shared_task
def fetch_movies():
    data = query_trakt('movies')
    Movie.objects.all().delete()
    for entry in data:
        tmdb = entry['movie']['ids']['tmdb']
        cover = fetch_cover('movie', tmdb)
        Movie.objects.create(
            name=entry['movie']['title'], year=entry['movie']['year'],
            watched=entry['watched_at'], tmdb=tmdb, cover=cover,
            url = 'http://www.imdb.com/title/{}/'.format(entry['movie']['ids']['imdb']))