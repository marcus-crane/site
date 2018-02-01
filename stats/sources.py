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

def update_books():
    url = ('https://www.goodreads.com/review/list?'
           'shelf=currently-reading&key={0}&id={1}'
           'v=2'.format(settings.GOODREADS, settings.GOODREADS_ID))
    data = query_service(url)
    root = ET.fromstring(data)[1]
    books = parsers.goodreads(root)
    db.save('books', books)

def update_music():
    url = ('http://ws.audioscrobbler.com/2.0/?'
           'method=user.getrecenttracks'
           '&user=sentryism&api_key={}'
           '&format=json&limit=10'.format(settings.LASTFM))
    data = query_service(url)
    music = parsers.lastfm(data)
    db.save('music', music)

def update_shows():
    url = 'https://api.trakt.tv/users/sentry/history/episodes'
    headers = { 'Content-Type': 'application/json',
                'trakt-api-version': '2',
                'trakt-api-key': settings.TRAKT }
    data = query_service(url, headers)
    episodes = parsers.trakt_shows()
    db.save('shows', shows)
