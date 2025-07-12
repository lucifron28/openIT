#!/bin/bash

echo "Syncing with remote repository..."

git pull origin main

# Update dependencies if package files changed
if git diff --name-only HEAD@{1} HEAD | grep -E "(requirements.txt|package.*\.json)"; then
    echo "Package files changed, updating dependencies..."
    ./scripts/install-deps.sh
fi

# Run migrations if models changed
if git diff --name-only HEAD@{1} HEAD | grep -E "models\.py|migrations/"; then
    echo "Database changes detected, running migrations..."
    ./scripts/migrate.sh
fi

echo "Sync complete!"
