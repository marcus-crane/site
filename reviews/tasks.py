from django.conf import settings
from django.utils.text import slugify
from celery import shared_task
import requests
import io
from PIL import Image, ImageFilter

@shared_task
def fetch_review_art(self):
    url = ('https://www.giantbomb.com/api/game/{}/?api_key={}'
           '&format=json'.format(self.gbid, settings.GIANTBOMB))
    r = requests.get(url, headers=settings.USER_AGENT)
    data = r.json()
    self.developer = data['results']['developers'][0]['name']
    self.title = data['results']['name']
    self.slug = slugify(self.title)
    self.cover = data['results']['image']['original_url']
    r = requests.get(data['results']['images'][0]['original'],
                     headers=settings.USER_AGENT)
    im = Image.open(io.BytesIO(r.content))
    im = im.filter(ImageFilter.GaussianBlur(3))
    im.save(settings.BASE_DIR + '/static/reviews/{}.png'.format(self.slug))
    self.backdrop = "/static/reviews/{}.png".format(self.slug)
    self.fresh = False
    return self