#!/bin/sh

# wait for RabbitMQ to start
sleep 10

su -m dockeruser -c "celery worker -A thingsimade"
