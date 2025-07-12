#!/bin/bash

# Initial project setup script
echo "Setting up project..."

# Create .env file from example if it doesn't exist
if [ ! -f "./backend/.env" ]; then
    echo "Creating .env file from example..."
    cp ./backend/.env.example ./backend/.env
    echo ".env file created. Please update it with your settings."
fi

# Make scripts executable
chmod +x scripts/*.sh

# Build containers without starting
echo "Building Docker containers..."
docker compose build

echo "Setting up database..."
./scripts/db-setup.sh

echo "Setup complete! Run './run.sh dev' to start development."
