#!/bin/bash

# Create Django superuser
echo "Creating Django superuser..."
docker compose exec backend python manage.py createsuperuser
