from .models import Book, Game, Movie, Song, Show
from stats import sources

import json

from bs4 import BeautifulSoup

def goodreads(data):
    """
    This parser restructures the Goodreads API response to
    both eliminate unneeded data and to be more human parsable.

    :param data: An XML string.
    :return: A dictionary object.
    """
    Book.objects.all().delete()
    for item in data:
        name = item[6].text
        image = item[7].text
        link = item[10].text
        author = item[21][0][1].text

        Book.objects.create(name=name, image=image,
                            link=link, author=author)

def howlongtobeat(data):
    """
    This parser restructures the How Long To Beat user games
    query to strip out any unneeded HTML elements

    :param data: An HTML snippet.
    :return: A dictionary object.
    """
    soup = BeautifulSoup(data, 'html.parser')
    Game.objects.all().delete()
    title_soup = soup.find_all("a", {"class": "text_green"})
    platform_soup = soup.find_all("span", {"class": "text_grey"})
    titles = [title.get_text().strip() for title in title_soup]
    platforms = [platform.get_text().strip() for platform in platform_soup]
    print(titles, platforms)
    for i in range(len(titles)):
        print(titles[i])
        Game.objects.create(name=titles[i], platform=platforms[i])


def lastfm(data):
    """
    This parser restructures the LastFM API response to
    both eliminate unneeded data and to be more human parsable.

    For more obscure tracks, an album cover may not be available
    so we just provide our own placeholder from the static folder.

    :param data: A serialised JSON string.
    :return: A dictionary object.
    """
    data = json.loads(data)
    Song.objects.all().delete()
    tracks = data['recenttracks']['track']
    for item in tracks:
        name = item['name']
        if not item['image'][3]['#text']:
            image = '/static/img/no_cover.png'
        else:
            image = item['image'][3]['#text']
        link = item['url']
        artist = item['artist']['#text']

        Song.objects.create(name=name, image=image,
                            link=link, artist=artist)


def trakt_movies(data):
    """
    This parser restructures the response from the
    Movies endpoint (of the Trakt API) to both
    eliminate unneeded data and to be more human parsable.

    As covers aren't provided in the Trakt response, we
    request them manually from TheMovieDB's API.

    :param data: A serialised JSON string.
    :return: A dictionary object.
    """
    data = json.loads(data)
    Movie.objects.all().delete()
    for item in data:
        tmdb = item['movie']['ids']['tmdb']
        imdb = item['movie']['ids']['imdb']

        name = item['movie']['title']
        image = sources.film_covers(tmdb)
        link = 'http://www.imdb.com/title/{}/'.format(imdb)
        year = item['movie']['year']

        Movie.objects.create(name=name, image=image,
                            link=link, year=year)


def trakt_shows(data):
    """
    This parser restructures the response from the
    TV endpoint (of the Trakt API) to both
    eliminate unneeded data and to be more human parsable.

    As show screenshots aren't provided in the Trakt response, we
    request them manually from TheTVDB's API.

    I would request them from TMDB too but TVDB is often more
    up to date despite usually be a more painful dev experience.

    :param data: A serialised JSON string.
    :return: A dictionary object.
    """
    data = json.loads(data)
    Show.objects.all().delete()
    for item in data:
        slug = item['show']['ids']['slug']
        season = item['episode']['season']
        number = item['episode']['number']

        name = item['episode']['title']
        series = item['show']['title']
        image = sources.show_covers(season, number, series)
        link = ('https://trakt.tv/shows/{}/seasons/{}/'
                'episodes/{}'.format(slug, season, number))

        Show.objects.create(name=name, image=image,
                            link=link, series=series)
