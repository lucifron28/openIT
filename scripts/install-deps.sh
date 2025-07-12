#!/bin/bash

# Install/update dependencies
echo "Installing dependencies..."

# Backend dependencies
echo "Installing backend dependencies..."
docker compose exec backend uv pip install -r requirements.txt

# Frontend dependencies
echo "Installing frontend dependencies..."
docker compose exec frontend npm install

echo "Dependencies installed!"
