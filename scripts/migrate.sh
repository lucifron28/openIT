#!/bin/bash

# Run Django migrations
echo "Running Django migrations..."
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
echo "Migrations complete!"
