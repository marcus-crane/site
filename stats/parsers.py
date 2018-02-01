import json

def goodreads(data):
    books = []
    for item in data:
        name = item[6].text
        image = item[7].text
        link = item[10].text
        author = item[21][0][1].text
        book = { 'name': name, 'image': image,
                 'link': link, 'author': author }
        books.append(book)
    return books

def lastfm(data):
    data = json.loads(data)
    music = []
    tracks = data['recenttracks']['track']
    for item in tracks:
        name = item['name']
        if not item['image'][3]['#text']:
            image = '/static/img/no_cover.png'
        else:
            image = item['image'][3]['#text']
        link = item['url']
        artist = item['artist']['#text']
        track = { 'name': name, 'image': image,
                  'link': link, 'artist': artist }
        music.append(track)
    return music
