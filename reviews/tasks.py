from django.conf import settings
from django.utils.text import slugify
from celery import shared_task
import requests

@shared_task
def fetch_review_art(self):
    url = ('https://www.giantbomb.com/api/game/{}/?api_key={}'
           '&format=json'.format(self.gbid, settings.GIANTBOMB))
    r = requests.get(url, headers=settings.USER_AGENT)
    data = r.json()
    self.developer = data['results']['developers'][0]['name']
    self.title = data['results']['name']
    self.slug = slugify(self.title)
    self.cover = data['results']['image']['medium_url']
    self.backdrop = data['results']['images'][0]['original']
    self.fresh = False
    return self