from celery.schedules import crontab

BROKER_URL = 'amqp://guest@localhost:5672//'

CELERYBEAT_SCHEDULE = {
    'update_books': {
        'task': 'tasks.update_books',
        'schedule': crontab(hour='*/6')
    },
    'update_movies': {
        'task': 'tasks.update_movies',
        'schedule': crontab(hour='*/4')
    },
    'update_music': {
        'task': 'tasks.update_music',
        'schedule': crontab(minute='*/5')
    },
    'update_shows': {
        'task': 'tasks.update_shows',
        'schedule': crontab(minute='*/20')
    }
}
