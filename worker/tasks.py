import sources

from celery import Celery

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

sources.books()
sources.movies()
sources.music()
sources.shows()

@celery.task
def update_books():
    sources.books()


@celery.task
def update_movies():
    sources.movies()


@celery.task
def update_music():
    sources.music()


@celery.task
def update_shows():
    sources.shows()
