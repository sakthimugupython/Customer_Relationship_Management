#!/bin/bash

# Build script for Render deployment
# This script is automatically run during deployment

set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking Django setup..."
python manage.py check

echo "Build completed successfully!"
