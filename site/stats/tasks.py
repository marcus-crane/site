from celery import shared_task
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thingsimade.settings')

import django
django.setup()

from .sources import books, movies, music, shows

@shared_task
def update_books():
    books()

@shared_task
def update_movies():
    movies()

@shared_task
def update_music():
    music()

@shared_task
def update_shows():
    shows()