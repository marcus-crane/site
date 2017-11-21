from django.conf import settings
from celery import shared_task

from .models import Album

import requests

@shared_task
def fetch_albums():
    def queryAPI():
        try:
            url = ('http://ws.audioscrobbler.com/2.0/?'
                   'api_key={}&format=json&method='
                   'user.getweeklyalbumchart'
                   '&user=sentryism'.format(settings.LAST_FM))
            r = requests.get(url)
            data = r.json()
            return data
        except Exception as error:
            print(error)

    try:
        data = queryAPI()
        albums = data['weeklyalbumchart']['album']
        for album in albums:
            name = album['name']
            artist = album['artist']['#text']
            cover = 'http://example.com'
            playcount = album['playcount']
            url = album['url']
            Album.objects.create(name=name, artist=artist,
                cover=cover, playcount=playcount, url=url)
    except Exception as error:
        print(error)