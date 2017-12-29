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

def fetch_episodes():
    def fetch_cover(tmdb_id, season, number):
        url = ('https://api.themoviedb.org/3/tv/{}/season/{}/episode/{}/images'
               '?api_key={}'.format(tmdb_id, season, number, settings.TMDB))
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            img = data['stills'][0]['file_path']
            return 'https://image.tmdb.org/t/p/w780' + img

    def insert_ep(episode):
        show = episode['show']['title']
        name = episode['episode']['title']
        watched = maya.parse(episode['watched_at']).datetime()
        season = episode['episode']['season']
        number = episode['episode']['number']
        tmdb_id = episode['show']['ids']['tmdb']
        cover = fetch_cover(tmdb_id, season, number)
        url = 'http://www.imdb.com/title/{}/'.format(episode['episode']['ids']['imdb'])
        Episode.objects.create(show=show, name=name, watched=watched,
                               season=season, number=number, tmdb=tmdb_id,
                               cover=cover, url=url)

    data = query_trakt('episodes')
    Episode.objects.all().delete()
    for episode in data:
        insert_ep(episode)

def fetch_movies():
    def fetch_cover(tmdb_id):
        url = ('https://api.themoviedb.org/3/movie/{}/images'
               '?api_key={}'.format(tmdb_id, settings.TMDB))
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            img = data['posters'][0]['file_path']
            return 'https://image.tmdb.org/t/p/w780' + img

    def insert_movie(entry):
        name = entry['movie']['title']
        year = entry['movie']['year']
        watched = entry['watched_at']
        tmdb = entry['movie']['ids']['tmdb']
        cover = fetch_cover(tmdb)
        url = 'http://www.imdb.com/title/{}/'.format(entry['movie']['ids']['imdb'])
        Movie.objects.create(name=name, year=year, watched=watched,
                             tmdb=tmdb, cover=cover, url=url)

    data = query_trakt('movies')
    Movie.objects.all().delete()
    for entry in data:
        insert_movie(entry)
