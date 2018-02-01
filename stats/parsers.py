import sources

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

def trakt_movies(data):
    data = json.loads(data)
    movies = []
    for item in data:
        tmdb = item['movie']['ids']['tmdb']
        imdb = item['movie']['ids']['imdb']

        name = item['movie']['title']
        image = sources.film_covers(tmdb)
        link = 'http://www.imdb.com/title/{}/'.format(imdb)
        year = item['movie']['year']

        movie = { 'name': name, 'image': image,
                  'link': link, 'year': year }
        movies.append(movie)
    return movies

def trakt_shows(data):
    data = json.loads(data)
    shows = []
    for item in data:
        tmdb = item['show']['ids']['tmdb']
        url = item['episode']['ids']['imdb']
        season = item['episode']['season']
        number = item['episode']['number']

        name = item['episode']['title']
        series = item['show']['title']
        image = sources.show_covers(tmdb, season, number, series)
        link = 'http://www.imdb.com/title/{}/'.format(url)

        show = { 'name': name, 'image': image,
                 'link': link, 'series': series }
        shows.append(show)
    return shows
