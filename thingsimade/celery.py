import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thingsimade.settings')

app = Celery('thingsimade')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	sender.add_periodic_task(30.0, stats.fetch_movies(), name='Fetch movies from Trakt')

@app.task
def test(arg):
	print(arg)
