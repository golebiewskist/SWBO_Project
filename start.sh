#!/bin/bash
set -e

echo "=== Applying database migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear

echo "=== Starting Gunicorn ==="
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 SWBO_Project.wsgi:application