from django.conf import settings
from django.shortcuts import render
import pendulum
import requests

from .models import Episode
from .models import Movie

def stats(request):
    def lastfm():
        try:
            url = ('http://ws.audioscrobbler.com/2.0/?'
                   'method=user.getrecenttracks'
                   '&user=sentryism&api_key={}'
                   '&format=json&limit=10'.format(settings.LAST_FM))
            r = requests.get(url)
            data = r.json()
            tracks = data['recenttracks']['track']
            music = {}
            for index, track in enumerate(tracks):
                scrobble = {}
                scrobble['album'] = track['album']['#text']
                scrobble['artist'] = track['artist']['#text']
                if track['image'][3]['#text'] is None:
                    scrobble['cover'] = 'http://via.placeholder.com/350x150'
                else:
                    scrobble['cover'] = track['image'][3]['#text']
                scrobble['name'] = track['name']
                scrobble['url'] = track['url']
                music[index] = scrobble
            return music
        except Exception as error:
            print(error)
            return render(request, '500.html')

    def steam():
        try:
            url = ('http://api.steampowered.com/IPlayerService/'
                   'GetRecentlyPlayedGames/v0001/?key={}'
                   '&steamid=76561197999386785'
                   '&format=json&limit=10'.format(settings.STEAM))
            r = requests.get(url)
            data = r.json()
            if data['response']['total_count'] == 0:
                return None
            else:
                data = data['response']['games']
            games = {}
            for index, game in enumerate(data):
                title = {}
                appid = game['appid']
                title['name'] = game['name']
                playtime = pendulum.interval(minutes=game['playtime_2weeks'])
                title['playtime'] = playtime.in_words(locale='en_us')
                if appid == 12230:
                    appid = 12100
                title['banner'] = ('https://steamcdn-a.akamaihd.net/steam/'
                                   'apps/{}/header.jpg'.format(appid))
                title['url'] = 'https://store.steampowered.com/app/{}/'.format(appid)
                games[index] = title
            return games
        except Exception as error:
            print(error)
            return render(request, '500.html')

    return render(request, 'stats/index.html', { 'albums': lastfm(), 'episodes': Episode.objects.all(), 'games': steam(), 'movies': Movie.objects.all()[:4] })
