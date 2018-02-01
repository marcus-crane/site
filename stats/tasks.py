import sources

from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@rabbitmq:5672//')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(21600, sources.books.s(), name="Update books every 6 hours")
    sender.add_periodic_task(14400, sources.movies.s(), name="Update movies every 4 hours")
    sender.add_periodic_task(300, sources.music.s(), name="Update music every 5 minutes")
    sender.add_periodic_task(1200, sources.shows.s(), name="Update shows every 20 minutes")
