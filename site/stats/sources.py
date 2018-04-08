import xml.etree.ElementTree as ET

from stats import parsers

from django.conf import settings
from pytvdbapi import api
import requests

def query_service(url, headers={}, payload={}):
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
    :return: A string or dictionary.
    """
    headers['User-Agent'] = settings.USER_AGENT
    if bool(payload):
        r = requests.post(url, headers=headers, data=payload)
    else:
        r = requests.get(url, headers=headers)
    if 'json' in headers['Content-Type']:
        return r.json()
    return r.text

def book_covers(title):
    url = ('https://goodreads.com/search/index.xml?key={0}'
           '&q={1}'.format(settings.GOODREADS, title))
    headers = {'Content-Type': 'application/xml'}
    try:
        data = query_service(url, headers)
        root = ET.fromstring(data)
        cover = root[1][6][0][8][3].text
        img = 'https://images.gr-assets.com/books/{}/{}'.format(
            cover.split('/')[4].replace('m', 'l'),
            cover.split('/')[5]
        )
    except Exception:
        img = 'https://static.thingsima.de/shared/img/no_cover.png'
    
    return img

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
    headers = {'Content-Type': 'application/json'}
    try:
        data = query_service(url, headers)
        poster = data['posters'][0]['file_path']
        img = 'https://image.tmdb.org/t/p/w500{}'.format(poster)
    except Exception:
        img = 'https://static.thingsima.de/shared/img/no_cover.png'

    return img

def game_data(title):
    """
    This function fetches game cover art and other data from Giant Bomb.

    It assumes that the first result which has the resource_type of game
    is going to be the correct entry.

    :param title: A string containing the name of a videogame.
    :return A dictionary containing a game name, image, id and release year
    """
    url = ('https://www.giantbomb.com/api/search?query={0}'
           '&api_key={1}&format=json'.format(title, settings.GIANTBOMB))
    headers = {'Content-Type': 'application/json'}
    game = {}
    try:
        data = query_service(url, headers)
        entries = data['results']
        entry = list(filter(lambda x: x['resource_type'] == 'game', entries))[0]
        game['img'] = entry['image']['super_url']
        game['link'] = entry['site_detail_url']
        game['name'] = entry['name']
        game['year'] = int(entry['original_release_date'][0:3])
    except Exception:
        game['img'] = 'https://static.thingsima.de/shared/img/no_cover.png'

    return game


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
        img = 'https://static.thingsima.de/shared/img/no_still.png'

    return img


def books():
    """
    Calling this kicks off everything required to store recently
    read books in the database.

    :return: N/A
    """
    url = ('https://www.goodreads.com/review/list?'
           'shelf=currently-reading&key={0}&id={1}'
           'v=2'.format(settings.GOODREADS, settings.GOODREADS_ID))
    headers = {'Content-Type': 'application/xml'}
    data = query_service(url, headers)
    root = ET.fromstring(data)[1]
    parsers.goodreads(root)

def games():
    """
    Calling this kicks off everything required to store recently
    played games in the database.

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
    watched movies in the database.

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
    listened music in the database.

    :return: N/A
    """
    url = ('http://ws.audioscrobbler.com/2.0/?'
           'method=user.getrecenttracks'
           '&user=sentryism&api_key={}'
           '&format=json&limit=10'.format(settings.LASTFM))
    headers = {'Content-Type': 'application/json'}
    data = query_service(url, headers)
    parsers.lastfm(data)


def shows():
    """
    Calling this kicks off everything required to store recently
    watched TV series in the database.

    :return: N/A
    """
    url = 'https://api.trakt.tv/users/sentry/history/episodes'
    headers = {'Content-Type': 'application/json',
               'trakt-api-version': '2',
               'trakt-api-key': settings.TRAKT}
    data = query_service(url, headers)
    parsers.trakt_shows(data)
