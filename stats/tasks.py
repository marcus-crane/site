from django.conf import settings
from celery import shared_task

from .models import Album

import requests

# def fetch_episodes():
#     def query_trakt():
#         headers = { 'Content-Type': 'application/json',
#                     'trakt-api-version': 2,
#                     'trakt-api-key': settings.TRAKT }
#         url = 'https://api.trakt.tv/users/sentry/history/episodes'
#         r = requests.get(url, headers=headers)
#         if r.status_code == 200:
#             return r.json()
    