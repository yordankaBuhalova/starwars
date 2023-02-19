#! /bin/sh

# prerequisites
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput

# start application
python manage.py runserver 0.0.0.0:8000
