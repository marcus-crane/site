#!/bin/sh

# Wait for RabbitMQ to start
sleep 10

cd site
su -c "celery worker -A thingsimade --beat --loglevel=info"
