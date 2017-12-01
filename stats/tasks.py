from django.conf import settings
from celery import shared_task

from .models import Album

import requests

@shared_task
def fetch_albums():
    def query_last_fm():
        try:
            headers = { 'User-Agent': 'tStatsUpdater/0.1 +https://thingsima.de/stats' }
            url = ('http://ws.audioscrobbler.com/2.0/?'
                   'api_key={}&format=json&method='
                   'user.getweeklyalbumchart'
                   '&user=sentryism'.format(settings.LAST_FM))
            r = requests.get(url, headers=headers)
            data = r.json()
            return data
        except Exception as error:
            print(error)

    # If the album has an MBID identifier, we can search the Internet Archive
    def fetch_ia_cover(mbid):
        try:
            headers = { 'User-Agent': 'tStatsUpdater/0.1 +https://thingsima.de/stats' }
            url = 'http://coverartarchive.org/release/{}'.format(mbid)
            r = requests.get(url, headers=headers)
            print(r.status_code)
            if r.status_code === 200:
                data = r.json()
                return data['images'][0]['image']
            else:
                return 'https://via.placeholder.com/300x300.jpg'
        except Exception as error:
            return 'https://via.placeholder.com/300x300.jpg'

    try:
        data = query_last_fm()
        albums = data['weeklyalbumchart']['album']
        for album in albums:
            name = album['name']
            artist = album['artist']['#text']
            cover = 'https://via.placeholder.com/300x300.jpg'
            playcount = int(album['playcount'])
            url = album['url']
            print(name, artist, cover, playcount, url)
            Album.objects.create(name=name, artist=artist,
                cover=cover, playcount=playcount, url=url)
    except Exception as error:
        print(error)