#!/bin/sh

# wait for PSQL to start
sleep 10

su -m dockeruser -c "python manage.py makemigrations"
su -m dockeruser -c "python manage.py migrate"
su -m dockeruser -c "python manage.py runserver 0.0.0.0:8000"
