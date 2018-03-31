#!/bin/sh

# Wait for postgres to spin up
sleep 10

cd site

su -c "python manage.py makemigrations"
su -c "python manage.py migrate"
su -c "/usr/local/bin/gunicorn thingsimade.wsgi:application -w 2 -b :8000"