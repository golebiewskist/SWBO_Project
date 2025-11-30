#!/bin/bash
set -e

echo "=== Checking database connection ==="
python -c "
import os
import django
from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection OK')
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
"

echo "=== Applying database migrations ==="
python manage.py migrate

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput --clear

echo "=== Starting Gunicorn ==="
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 SWBO_Project.wsgi:application