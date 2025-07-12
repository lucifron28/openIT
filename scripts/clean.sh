#!/bin/bash

# Clean up Docker resources
echo "Cleaning up Docker resources..."

# Stop all services
docker compose down

# Remove unused images, containers, and networks
docker system prune -f

# Remove node_modules volume if it exists
docker volume rm drf-jwt_node_modules 2>/dev/null || true

echo "Cleanup complete!"
