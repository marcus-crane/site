from django.conf import settings
from django.shortcuts import get_list_or_404
from django.shortcuts import render
import pendulum
import requests

from .models import Album

def stats(request):
    # def lastfm():
    #     return Album.objects.all()

    def steam():
        try:
            url = ('http://api.steampowered.com/IPlayerService/'
                   'GetRecentlyPlayedGames/v0001/?key={}'
                   '&steamid=76561197999386785'
                   '&format=json&limit=10'.format(settings.STEAM))
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
            return games
        except Exception as error:
            return render(request, '500.html')

    return render(request, 'stats/index.html', { 'games': steam() })