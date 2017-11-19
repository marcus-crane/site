from django.conf import settings
from django.shortcuts import render
import pendulum
import requests

def lastfm(request):
    try:
        url = ('http://ws.audioscrobbler.com/2.0/?'
               'method=user.getrecenttracks'
               '&user=sentryism&api_key={}'
               '&format=json&limit=15'.format(settings.LAST_FM))
        r = requests.get(url)
        data = r.json()
        tracks = data['recenttracks']['track']
        music = {}
        for index, track in enumerate(tracks):
            scrobble = {}
            scrobble['album'] = track['album']['#text']
            scrobble['artist'] = track['artist']['#text']
            scrobble['image'] = track['image'][3]['#text']
            scrobble['name'] = track['name']
            scrobble['url'] = track['url']
            music[index] = scrobble
        return render(request, 'stats/lastfm.html', { 'music': music })
    except Exception as error:
        return render(request, '500.html')

def steam(request):
    try:
        url = ('http://api.steampowered.com/IPlayerService/'
               'GetRecentlyPlayedGames/v0001/?key={}'
               '&steamid=76561197999386785'
               '&format=json'.format(settings.STEAM))
        r = requests.get(url)
        data = r.json()
        data = data['response']['games']
        games = {}
        for index, game in enumerate(data):
            title = {}
            title['id'] = game['appid']
            title['name'] = game['name']
            playtime = pendulum.interval(minutes=game['playtime_2weeks'])
            title['playtime'] = playtime.in_words(locale='en_us')
            title['banner'] = ('http://cdn.edgecast.steamstatic.com/steam/'
                               'apps/{}/header.jpg'.format(game['appid']))
            games[index] = title
        print(games)
        return render(request, 'stats/steam.html', { 'games': games })
    except Exception as error:
        return render(request, '500.html')