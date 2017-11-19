from django.shortcuts import render
import requests

def lastfm(request):
    try:
        url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=sentryism&api_key={}&format=json'.format(key)
        r = requests.get(url)
        data = r.json()
        tracks = data["recenttracks"]["track"]
        music = {}

        for index, track in enumerate(tracks):
            scrobble = {}
            scrobble['album'] = track["album"]["#text"]
            scrobble['artist'] = track["artist"]["#text"]
            scrobble['image'] = track["image"][3]["#text"]
            scrobble['name'] = track["name"]
            scrobble['url'] = track["url"]
            music[index] = scrobble

        print(music)
        return render(request, 'stats/lastfm.html', { 'music': music })
    except Exception as error:
        print('something broke', error)
        return render(request, 'stats/lastfm.html')