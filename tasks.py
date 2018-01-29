import settings
from utils import update_books, update_movies, update_music, update_shows

from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672//')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(21600, update_books.s(), name="Update books every 6 hours")
    sender.add_periodic_task(14400, update_movies.s(), name="Update movies every 4 hours")
    sender.add_periodic_task(300, update_music.s(), name="Update music every 5 minutes")
    sender.add_periodic_task(1200, update_shows.s(), name="Update shows every 20 minutes")
    sender.add_periodic_task(60, test.s('world'), name="Say world every 60 seconds")

@app.task
def test(arg):
    print(arg)
