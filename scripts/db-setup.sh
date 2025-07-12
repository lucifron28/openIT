#!/bin/bash

# Database setup script
echo "Setting up database..."

# Start only the database service
docker-compose up -d db

# Wait for database to be ready
echo "Waiting for database to be ready..."
until docker-compose exec db pg_isready -U postgres; do
    sleep 1
done

# Run migrations
echo "Running Django migrations..."
docker-compose run --rm backend python manage.py makemigrations
docker-compose run --rm backend python manage.py migrate

echo "Database setup complete!"
