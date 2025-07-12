#!/bin/bash

# Django shell access
echo "Starting Django shell..."
docker compose exec backend python manage.py shell
