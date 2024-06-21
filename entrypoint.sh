#!/bin/bash

# Wait for PostgreSQL to be ready (optional but recommended)
until nc -zv $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done

# Apply Django migrations
echo "Applying Django migrations..."
python manage.py makemigrations
python manage.py migrate

# Start the Django server or other necessary services
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
