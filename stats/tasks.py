from django.conf import settings
from celery import shared_task

from .models import Episode

import maya
import requests

@shared_task
def fetch_episodes():
    def query_trakt():
        headers = { 'Content-Type': 'application/json',
                    'trakt-api-version': '2',
                    'trakt-api-key': settings.TRAKT }
        url = 'https://api.trakt.tv/users/sentry/history/episodes'
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.json()

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
        name=episode['episode']['title']
        watched=maya.parse(episode['watched_at']).datetime()
        season=episode['episode']['season']
        number=episode['episode']['number']
        tmdb_id=episode['show']['ids']['tmdb']
        cover=fetch_cover(tmdb_id, season, number)
        Episode.objects.create(show=show, name=name, watched=watched,
                               season=season, number=number, tmdb=tmdb_id,
                               cover=cover)

    data = query_trakt()
    Episode.objects.all().delete()
    for episode in data:
        insert_ep(episode)