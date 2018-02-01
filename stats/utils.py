from classes import Book, Episode, Movie, Song
import settings

from pytvdbapi import api
import requests

import xml.etree.ElementTree as ET

def update_books():
    def query_goodreads():
        url = ('https://www.goodreads.com/review/list?'
               'shelf=currently-reading&key={0}&id={1}'
               'v=2'.format(settings.GOODREADS, settings.GOODREADS_ID))
        headers = { 'User-Agent': settings.USER_AGENT }
        r = requests.get(url, headers=headers)
        return r.text

    def fetch_titles(books):
        titles = []
        for book in books:
            name = book[6].text
            image = book[7].text
            link = book[10].text
            author = book[21][0][1].text

            entry = Book(name, image, link, author)
            entry = entry.export()
            titles.append(entry)
        return titles

    data = query_goodreads()
    root = ET.fromstring(data)
    books = fetch_titles(root[1])
    generate_json('books', books)

def update_movies():
    def fetch_movies(data):
        movies = []
        for entry in data:
            tmdb = entry['movie']['ids']['tmdb']
            imdb = entry['movie']['ids']['imdb']

            name = entry['movie']['title']
            image = fetch_cover('movie', tmdb)
            link = 'http://www.imdb.com/title/{}/'.format(imdb)
            year = entry['movie']['year']

            movie = Movie(name, image, link, year)
            movie = movie.export()
            movies.append(movie)
        return movies

    data = query_trakt('movies')
    movies = fetch_movies(data)
    generate_json('movies', movies)


def update_music():
    def query_lastfm():
        url = ('http://ws.audioscrobbler.com/2.0/?'
               'method=user.getrecenttracks'
               '&user=sentryism&api_key={}'
               '&format=json&limit=10'.format(settings.LASTFM))
        headers = { 'User-Agent': settings.USER_AGENT }
        r = requests.get(url, headers=headers)
        return r.json()

    def fetch_songs(data):
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
            song = Song(name, image, link, artist)
            song = song.export()
            music.append(song)
        return music

    data = query_lastfm()
    songs = fetch_songs(data)
    generate_json('music', songs)

def query_trakt(endpoint):
    headers = { 'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': settings.TRAKT,
                'User-Agent': settings.USER_AGENT }
    url = 'https://api.trakt.tv/users/sentry/history/{}'.format(endpoint)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()

def fetch_cover(type, tmdb_id, season=None, number=None, series=None):
    if type == 'movie':
        url = ('https://api.themoviedb.org/3/movie/{}/images'
               '?api_key={}'.format(tmdb_id, settings.TMDB))
        headers = { 'User-Agent': settings.USER_AGENT }
        r = requests.get(url, headers=headers)
        try:
            data = r.json()
            poster = data['posters'][0]['file_path']
            img = 'https://image.tmdb.org/t/p/w500{}'.format(poster)
        except:
            img = '/static/img/no_cover.png'

    if type == 'show':
        db = api.TVDB(settings.TVDB)
        result = db.search(series, 'en')
        try:
            show = result[0]
            url = show[season][number].filename
            if url != '':
                img = 'https://www.thetvdb.com/banners/{}'.format(url)
            else:
                raise
        except:
            img = '/static/img/no_still.png'

    return img

def update_shows():
    def fetch_shows(data):
        shows = []
        for entry in data:
            tmdb = entry['show']['ids']['tmdb']
            url = entry['episode']['ids']['imdb']
            season = entry['episode']['season']
            number = entry['episode']['number']

            series = entry['show']['title']
            name = entry['episode']['title']
            image = fetch_cover('show', tmdb, season, number, series)
            link = 'http://www.imdb.com/title/{}/'.format(url)

            episode = Episode(name, image, link, series)
            episode = episode.export()
            shows.append(episode)
        return shows

    data = query_trakt('episodes')
    shows = fetch_shows(data)
    generate_json('shows', shows)
