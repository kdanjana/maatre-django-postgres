#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :8090 --workers 3 --master --enable-threads --module ecommerce.wsgi