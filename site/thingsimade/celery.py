import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thingsimade.settings')

import django
django.setup()

from celery import Celery
from celery.schedules import crontab
from celery.signals import celeryd_init
from celery.utils.log import get_task_logger

from stats import tasks

logger = get_task_logger(__name__)

app = Celery('thingsimade')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-books-every-6-hours': {
        'task': 'stats.tasks.update_books',
        'schedule': crontab(hour='*/6')
    },
    'update-movies-every-3-hours': {
        'task': 'stats.tasks.update_movies',
        'schedule': crontab(hour='*/3')
    },
    'update-music-every-5-minutes': {
        'task': 'stats.tasks.update_music',
        'schedule': crontab(minute='*/5')
    },
    'update-shows-every-20-minutes': {
        'task': 'stats.tasks.update_shows',
        'schedule': crontab(minute='*/20')
    },
}

logger.info("Online and logged on")

@celeryd_init.connect
def configure_workers(sender=None, conf=None, **kwargs):
    logger.info('Workers are being configured')
    tasks.update_books()
    tasks.update_movies()
    tasks.update_music()
    tasks.update_shows()