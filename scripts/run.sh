#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn ecommerce.wsgi:application -c gunicorn_config.py