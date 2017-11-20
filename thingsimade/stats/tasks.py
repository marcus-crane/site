from celery import shared_task
import requests

from thingsimade.stats.models import Album

@shared_task
def fetch_recent_albums():
    def queryAPI(endpoint):
        try:
            base_url = ('http://ws.audioscrobbler.com/2.0/?'
                        'api_key={}&format=json'.format(
                        endpoint, settings.LAST_FM))
            if endpoint == 'albums':
                url = (base_url + '&method='
                       'user.getweeklyalbumchart'
                       '&user=sentryism')
            if endpoint == 'getinfo':
                url = (base_url + '&method='
                       'album.getinfo&artist='
                       '{}&album={}'.format(
                        artist, album))
            r = requests.get(url)
            data = r.json()
            return data
        except Exception as error:
            print(error)

    def fetch_cover(artist, album):
        query = queryAPI('getinfo', artist, album)
        image = query['album']['image'][3]['#text']
        return image

    try:
        data = queryAPI('albums')
        albums = data['weeklyalbumchart']['album']
        for album in albums:
            name = album['name']
            artist = album['artist']['#text']
            cover = fetch_cover(artist, name)
            playcount = album['playcount']
            url = album['url']
            Album.objects.create(name=name, artist=artist,
                cover=cover, playcount=playcount, url=url)
    except Exception as error:
        print(error)

