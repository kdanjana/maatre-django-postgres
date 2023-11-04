#!/bin/sh


set -e
# We'll check if database is ready to connect or not
echo "Waiting for database..."
echo DB_NAME: ${DB_NAME}
echo DB_HOST: ${DB_HOST}
echo DB_PORT: ${PORT}
while ! nc -z ${DB_HOST} ${PORT}; do sleep 1; done
echo "Connected to database."

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn ecommerce.wsgi:application -c gunicorn_config.py --log-level=debug --access-logfile=- --error-logfile=-