#!/bin/bash

# Database reset script
echo "This will reset the database and all data will be lost!"
read -p "Are you sure? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Stopping and removing database container..."
    docker-compose down
    docker volume rm drf-jwt_postgres_data 2>/dev/null || true
    
    echo "Recreating database..."
    ./scripts/db-setup.sh
    
    echo "Database reset complete!"
else
    echo "Database reset cancelled."
fi
