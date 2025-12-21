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

# Install Python dependencies (Vercel uses pip, not uv)
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set environment for S3 static files on Vercel
export USE_S3_FOR_STATIC=True
export VERCEL=1

# Collect static files (will upload to S3 when USE_S3_FOR_STATIC=True)
echo "Collecting static files to S3..."
python manage.py collectstatic --noinput --clear

echo "==================================="
echo "Build completed successfully!"
echo "Static files uploaded to S3"
echo "==================================="
