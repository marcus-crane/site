from classes import Book, Episode, Movie, Song
import settings

from pytvdbapi import api
import requests

import xml.etree.ElementTree as ET


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
