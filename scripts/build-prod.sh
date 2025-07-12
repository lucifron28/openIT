#!/bin/bash

# Build production images
echo "Building production images..."

# Build frontend for production
docker compose exec frontend npm run build

# You can add production Docker builds here later
echo "Production build complete!"
