#!/bin/bash

echo "Running Migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
gunicorn week4.wsgi --bind 0.0.0.0:$PORT
