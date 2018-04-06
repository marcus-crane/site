import xml.etree.ElementTree as ET

from stats import parsers

from django.conf import settings
from pytvdbapi import api
import requests

def query_service(url, headers={}, payload=None):
    """
    A generalised function that handles making requests and
    injecting a user agent header.

    No assumption is made about the Content-Type being returned.
    You'll need to perform any required parsing in the sources/parser
    function (eg json.loads or xml.etree.ElementTree)

    :param url: A string containing the URL to be requested.
    :param method: A string containing either GET or POST
    :param headers: A dictionary containing any other required headers.
    :param payload: A dictionary containing data to send
    :return: A serialised string.
    """
    headers['User-Agent'] = settings.USER_AGENT
    if payload is not None:
        r = requests.post(url, headers=headers, data=payload)
    else:
        r = requests.get(url, headers=headers)
    return r.text


def film_covers(tmdb):
    """
    This function fetches film posters, sometimes called covers,
    from TheMovieDB.

    In the event that a cover can't be found, a local placeholder
    will be used instead.

    I've never actually had it trigger though
    since film posters are seemingly always available.

    :param tmdb: A string containing an ID for TheMovieDB entry.
    :return: A string containing a URL to an image.
    """
    url = ('https://api.themoviedb.org/3/movie/{}/images'
           '?api_key={}'.format(tmdb, settings.TMDB))
    headers = {'User-Agent': settings.USER_AGENT}
    r = requests.get(url, headers=headers)
    try:
        data = r.json()
        poster = data['posters'][0]['file_path']
        img = 'https://image.tmdb.org/t/p/w500{}'.format(poster)
    except Exception:
        img = '/static/img/no_cover.png'

    return img


def show_covers(season, number, series):
    """
    This function fetches show screenshots, called covers in this
    instance. You can think of them as thumbnails but I needed a
    word that could be generalised for movies and TV show images.

    In the event that a cover can't be found, a local placeholder
    will be used instead.

    This often triggers for recently aired shows but it's usually
    fixed within a day or so. You'll probably find anime is the
    most lacking since there's less eyeballs on fresh seasonal
    releases compared to eg; a Netflix series.

    :param season: A string containing the season number of the
                   requested episode.
    :param number: A string containing the episode number of the
                   requested episode.
    :param series: A string containing the name of the requested
                   show.
    :return: A string containing a URL to an image.
    """
    tvdb = api.TVDB(settings.TVDB)
    result = tvdb.search(series, 'en')
    try:
        show = result[0]
        url = show[season][number].filename
        if url != '':
            img = 'https://www.thetvdb.com/banners/{}'.format(url)
        else:
            raise Exception
    except Exception:
        img = '/static/img/no_still.png'

    return img


def books():
    """
    Calling this kicks off everything required to store recently
    read books in CouchDB.

    :return: N/A
    """
    url = ('https://www.goodreads.com/review/list?'
           'shelf=currently-reading&key={0}&id={1}'
           'v=2'.format(settings.GOODREADS, settings.GOODREADS_ID))
    data = query_service(url)
    root = ET.fromstring(data)[1]
    parsers.goodreads(root)

def games():
    """
    Calling this kicks off everything required to store recently
    played games in the DB.

    :return: N/A
    """
    payload = {'n': settings.HLTB, 'playing': '1'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = 'https://howlongtobeat.com/user_games_list.php'
    data = query_service(url, headers=headers, payload=payload)
    parsers.howlongtobeat(data)


def movies():
    """
    Calling this kicks off everything required to store recently
    watched movies in CouchDB.

    :return: N/A
    """
    url = 'https://api.trakt.tv/users/sentry/history/movies'
    headers = {'Content-Type': 'application/json',
               'trakt-api-version': '2',
               'trakt-api-key': settings.TRAKT}
    data = query_service(url, headers)
    parsers.trakt_movies(data)


def music():
    """
    Calling this kicks off everything required to store recently
    listened music in CouchDB.

    :return: N/A
    """
    url = ('http://ws.audioscrobbler.com/2.0/?'
           'method=user.getrecenttracks'
           '&user=sentryism&api_key={}'
           '&format=json&limit=10'.format(settings.LASTFM))
    data = query_service(url)
    parsers.lastfm(data)


def shows():
    """
    Calling this kicks off everything required to store recently
    watched TV series in CouchDB.

    :return: N/A
    """
    url = 'https://api.trakt.tv/users/sentry/history/episodes'
    headers = {'Content-Type': 'application/json',
               'trakt-api-version': '2',
               'trakt-api-key': settings.TRAKT}
    data = query_service(url, headers)
    parsers.trakt_shows(data)
