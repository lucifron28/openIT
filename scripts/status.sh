#!/bin/bash

# Show development environment status
echo "Development Environment Status"
echo "================================="

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo "Services running:"
    docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "Access URLs:"
    echo "   Frontend: http://localhost:5173"
    echo "   Backend:  http://localhost:8000"
    echo "   Admin:    http://localhost:8000/admin"
    echo "   Database: localhost:5433"
else
    echo "No services running"
    echo "Run './run.sh dev' to start development environment"
fi
