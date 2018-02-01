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

def update_music():
    url = ('http://ws.audioscrobbler.com/2.0/?'
           'method=user.getrecenttracks'
           '&user=sentryism&api_key={}'
           '&format=json&limit=10'.format(settings.LASTFM))
    data = query_service(url)
    songs = parsers.lastfm(data, True)
    db.reset_table('music')
    for song in songs:
        db.insert('music', song)
