import sources

import json


def goodreads(data):
    """
    This parser restructures the Goodreads API response to
    both eliminate unneeded data and to be more human parsable.

    :param data: An XML string.
    :return: A dictionary object.
    """
    books = []
    for item in data:
        name = item[6].text
        image = item[7].text
        link = item[10].text
        author = item[21][0][1].text
        book = {'name': name, 'image': image,
                'link': link, 'author': author}
        books.append(book)
    return books


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
    music = []
    tracks = data['recenttracks']['track']
    for item in tracks:
        name = item['name']
        if not item['image'][3]['#text']:
            image = '/img/no_cover.png'
        else:
            image = item['image'][3]['#text']
        link = item['url']
        artist = item['artist']['#text']
        track = {'name': name, 'image': image,
                 'link': link, 'artist': artist}
        music.append(track)
    return music


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
    movies = []
    for item in data:
        tmdb = item['movie']['ids']['tmdb']
        imdb = item['movie']['ids']['imdb']

        name = item['movie']['title']
        image = sources.film_covers(tmdb)
        link = 'http://www.imdb.com/title/{}/'.format(imdb)
        year = item['movie']['year']

        movie = {'name': name, 'image': image,
                 'link': link, 'year': year}
        movies.append(movie)
    return movies


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
    shows = []
    for item in data:
        slug = item['show']['ids']['slug']
        season = item['episode']['season']
        number = item['episode']['number']

        name = item['episode']['title']
        series = item['show']['title']
        image = sources.show_covers(season, number, series)
        link = ('https://trakt.tv/shows/{}/seasons/{}/'
                'episodes/{}'.format(slug, season, number))

        show = {'name': name, 'image': image,
                'link': link, 'series': series}
        shows.append(show)
    return shows
