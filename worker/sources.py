import connector
import parsers
import settings

import xml.etree.ElementTree as ET

from pytvdbapi import api
import requests

db = connector.Database()

def query_service(url, headers={}):
    headers['User-Agent'] = settings.USER_AGENT
    r = requests.get(url, headers=headers)
    return r.text

def film_covers(tmdb):
    url = ('https://api.themoviedb.org/3/movie/{}/images'
           '?api_key={}'.format(tmdb, settings.TMDB))
    headers = { 'User-Agent': settings.USER_AGENT }
    r = requests.get(url, headers=headers)
    try:
        data = r.json()
        poster = data['posters'][0]['file_path']
        img = 'https://image.tmdb.org/t/p/w500{}'.format(poster)
    except:
        img = '/static/img/no_cover.png'

    return img

def show_covers(season, number, series):
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

def books():
    url = ('https://www.goodreads.com/review/list?'
           'shelf=currently-reading&key={0}&id={1}'
           'v=2'.format(settings.GOODREADS, settings.GOODREADS_ID))
    data = query_service(url)
    root = ET.fromstring(data)[1]
    books = parsers.goodreads(root)
    db.save('books', books)

def movies():
    url = 'https://api.trakt.tv/users/sentry/history/movies'
    headers = { 'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': settings.TRAKT }
    data = query_service(url, headers)
    movies = parsers.trakt_movies(data)
    db.save('movies', movies)


def music():
    url = ('http://ws.audioscrobbler.com/2.0/?'
           'method=user.getrecenttracks'
           '&user=sentryism&api_key={}'
           '&format=json&limit=10'.format(settings.LASTFM))
    data = query_service(url)
    music = parsers.lastfm(data)
    db.save('music', music)

def shows():
    url = 'https://api.trakt.tv/users/sentry/history/episodes'
    headers = { 'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': settings.TRAKT }
    data = query_service(url, headers)
    shows = parsers.trakt_shows(data)
    db.save('shows', shows)
