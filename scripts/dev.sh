#!/bin/bash

# Development startup script
echo "Starting development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start all services
echo "Building and starting services..."
docker compose up --build

echo "Development environment started!"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "Database: localhost:5433"
