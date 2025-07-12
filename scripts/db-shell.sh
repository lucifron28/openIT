#!/bin/bash

# Database shell access
echo "Connecting to database shell..."
docker compose exec db psql -U postgres -d backend
