#!/bin/bash

# Build script for Vercel/serverless deployment
# This script runs during the build phase to prepare static assets

set -e

echo "==================================="
echo "Building Event Horizon for Vercel"
echo "==================================="

# Install Node dependencies if needed
if [ -f "package.json" ]; then
    echo "Installing Node.js dependencies..."
    npm install
    
    echo "Building Tailwind CSS..."
    npm run build:css
else
    echo "No package.json found, skipping Node.js setup"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
uv pip install --upgrade pip
uv pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
uv run python manage.py collectstatic --noinput --clear

echo "==================================="
echo "Build completed successfully!"
echo "==================================="
