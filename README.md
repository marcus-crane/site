# thingsima.de

# Summary

This is my personal site built using [Django 2.0](https://docs.djangoproject.com/en/2.0/releases/2.0/) and a number of other dependencies. I'll be detailing all of the pieces you'll need to get this project up and running in the following sections.

Briefly, my site has a:

* Blog, for writing whatever I feel like B)
* Contact page, which emails myself with whatever messages a visitor decides to leave
* Stats page, displaying movies, music, tv and steam titles

Those are currently the main components. The main goal of my site isn't to be a serious portfolio piece but just something that I can hack on and have fun with!

# Dependencies

## Python + Dependencies

In order to get this site up and running, you'll need a version of [Python 3](https://www.python.org/downloads/), preferably recent. Anything above `3.0` should be fine but I haven't tested that claim in the slightest.

Once you've got Python setup, you can install the required modules with `pip install -r requirements`. The suggested way is to set up a [virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) as opposed to just installing modules right into your system setup.

## RabbitMQ / Redis

In addition to the required [PyPi](https://pypi.python.org/) modules, you'll also need a [RabbitMQ](https://www.rabbitmq.com/) server for use with [Celery](www.celeryproject.org/). As I understand it, you can also fairly easily use [Redis](https://redis.io/) as a drop in replacement but you'll have to look that up yourself. I assume as long as you map the ports correctly, it'll "just work".

Personally, I can recommend installing [Docker](https://www.docker.com/) and running the official RabbitMQ docker image, found [here](https://hub.docker.com/_/rabbitmq) and installed by running `docker pull rabbitmq`. Once that's done, I just map the Docker ports to their respective local ports. For example, docker port `5672` -> local port `5672` and so on.

## Celery

Now that you've got an [AMPQ](https://en.wikipedia.org/wiki/Advanced_Message_Queuing_Protocol) messaging broker (rabbitmq or redis) installed and running, it's time to move back to the project and boot up the Celery module.

You'll want this running in the background in its own terminal window for the duration of your local testing. Assuming your current directory is inside the `site` folder, run `celery -A thingsimade worker --loglevel=info` and Celery will boot up and connect with RabbitMQ/Redis.

Once that's running, you should see similar output in your Celery window:

```py
[tasks]
  . stats.tasks.fetch_movies
  . stats.tasks.fetch_shows
  . thingsimade.celery.debug_task

[2017-12-29 20:51:40,486: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
```

## API Keys

One aspect of my site is that it's an excuse to put the API keys I've collected over the years to use. Currently, you'll need to request a key from the following sites:

* [Last.FM](https://www.last.fm/api/account/create)
* [Recaptcha V2](https://www.google.com/recaptcha/admin) (public + private)
* [Steam](http://steamcommunity.com/dev/apikey)
* [TheMovieDB](https://www.themoviedb.org/settings/api)
* [Trakt](https://trakt.tv/oauth/applications/new)

I've linked to the exact API key generation page for each service but you'll need to create accounts in the first place. You can also feel free to strip out any services you don't want of course. They only appear in the following files: `contact/views.py`, `stats/tasks.py` and `thingsimade/settings.py`

All of the required API keys will need to go in a `keys.ini` file located in the `site/thingsimade` folder. You can refer to the `keys_ex.ini` dummy file in order to see the required layout.

## Database migration

None of those keys are useful without a database to store their data in. For now, the site just runs on `sqlite3` because It Works™ and it barely receives any load. I'll eventually switch it to Postgres when I get more than like 6 visitors a year.

Running `python manage.py migrate` should be all you need to create an initial database. If you want some actual data for the stats page, enter `python manage.py shell` and do the following:

```py
from stats.tasks import *
fetch_movies.delay()
fetch_shows.delay()
```

You can run those two functions normally ie: `fetch_movies()` but running them with the added delay will offload them to Celery and process the queries in the background, which is a good way to check your earlier setup was correct.

You'll also want to create a user in order to access the admin panel located at [http://localhost:8000/admin](http://localhost:8000/admin) by running `python manage.py createsuperuser` and following the prompts.

# Running it

In order to spark up the development server, `cd` into `site` and run `python manage.py runserver` to host the site on `http://localhost:8000`.

# Is that all?

I think so? 

I've still got a bunch more stuff to set up but this README should be enough to get you running if you want to have a look around. Alternatively, you can just visit it live at [https://thingsima.de](https://thingsima.de)

Big thanks to

* [Adam Morse](https://github.com/mrmrs) + contributors for the [Tachyons](http://tachyons.io/) project for making CSS not as hellish as it normally is for me.
* [Dolphin Emulator](https://dolphin-emu.org) for releasing the [source](https://github.com/dolphin-emu/www) of their django site which got me interested in it in the first place. It's not exactly a great codebase by any standard but it was a nice example when I had no idea what the hell was going on.

# Is Django any good?

Yeah, I like it. It's a nice excuse to get better with Python too!