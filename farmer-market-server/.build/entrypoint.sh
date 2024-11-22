#!/bin/sh

python manage.py migrate --no-input

# python manage.py collectstatic --noinput

# DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

if [[ $DEBUG -eq 0 ]]; then
# production mode
#   daphne -b 0.0.0.0 -p 8010 sfb_market_backend.asgi:application &
  gunicorn farmer_market_server.wsgi:application --bind 0.0.0.0:8000
else

#   daphne -b 0.0.0.0 -p 8010 sfb_market_backend.asgi:application &
  python manage.py runserver 0.0.0.0:8000

fi
