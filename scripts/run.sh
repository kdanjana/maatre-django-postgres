#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn todoapp.wsgi:application -c gunicorn_config.py