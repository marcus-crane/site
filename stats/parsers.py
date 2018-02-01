import json

def lastfm(data, is_json):
    if is_json:
        data = json.loads(data)
    music = []
    tracks = data['recenttracks']['track']
    for track in tracks:
        name = track['name']
        if not track['image'][3]['#text']:
            image = '/static/img/no_cover.png'
        else:
            image = track['image'][3]['#text']
        link = track['url']
        artist = track['artist']['#text']
        song = { 'name': name, 'image': image,
                 'link': link, 'artist': artist }
        music.append(song)
    return music
