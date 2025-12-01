#!/bin/bash

# This script contains helpful commands for Render deployment

# View logs
# render logs --service-id=YOUR_SERVICE_ID

# Deploy specific branch
# git push origin main  # This will auto-trigger deployment if connected to GitHub

# Remote shell access
# render shell --service-id=YOUR_SERVICE_ID

# Common Management Commands (run via Render shell or local):

# Create superuser
# python manage.py createsuperuser

# Run migrations
# python manage.py migrate

# Collect static files
# python manage.py collectstatic --noinput

# Create database backup
# python manage.py dumpdata > backup.json

# Restore from backup
# python manage.py loaddata backup.json

# Check for issues
# python manage.py check

# Test email configuration
# python manage.py shell
# >>> from django.core.mail import send_mail
# >>> send_mail('Subject', 'Message', 'from@example.com', ['to@example.com'])

# Database management:
# PostgreSQL connection string format for Render:
# postgresql://username:password@hostname:port/database

# Environment variables to set in Render:
# DEBUG=False
# SECRET_KEY=your-unique-secret-key
# ALLOWED_HOSTS=yourapp.render.com,www.yourapp.render.com
# DATABASE_URL=postgresql://... (if using PostgreSQL)
