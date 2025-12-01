## Deployment Guide for Render

This guide explains how to deploy your CRM System to Render.com.

### Prerequisites
- GitHub account with your project repository
- Render.com account
- Project must be pushed to GitHub

### Step 1: Prepare for Deployment

Before deploying, ensure:
1. All static files are collected: `python manage.py collectstatic --noinput`
2. `.env` file is created with production values (DO NOT push to GitHub)
3. `requirements.txt` is up to date
4. All files are committed to Git

### Step 2: Create Environment Variables on Render

In your Render service settings, add these environment variables:

```
DEBUG=False
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=yourdomain.render.com,www.yourdomain.render.com
```

### Step 3: Deploy to Render

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Fill in the following:
   - **Name**: crm-system (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn crm_management.wsgi`
   - **Plan**: Free tier works for testing

5. Add environment variables from Step 2
6. Click "Create Web Service"

### Step 4: Configure Database (Optional)

For production, use PostgreSQL instead of SQLite:

1. In Render dashboard, create a PostgreSQL database
2. Copy the connection string
3. Add to environment variables: `DATABASE_URL=<your-postgres-url>`
4. Update `settings.py` to use DATABASE_URL (see below)

### Static Files Setup

The project is configured to:
1. Use WhiteNoise middleware for serving static files
2. Compress and cache static files for performance
3. Collect static files during deployment

Static files include:
- Bootstrap CSS and JavaScript
- Bootstrap Icons
- Custom CSS from base.html

### Troubleshooting

**CSS/Images not loading:**
- Ensure `collectstatic` runs during build
- Check that WhiteNoiseMiddleware is in MIDDLEWARE
- Verify STATICFILES_STORAGE is set correctly

**Debug mode issues:**
- Always set DEBUG=False in production
- Check SECRET_KEY is properly set
- Verify ALLOWED_HOSTS includes your domain

**Database errors:**
- For PostgreSQL: Install psycopg2-binary (included in requirements.txt)
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`

### Local Development

To test production settings locally:

1. Create `.env` file:
```
DEBUG=False
SECRET_KEY=test-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

2. Run: `python manage.py runserver`

### Files Included for Deployment

- **Procfile**: Specifies how to run the app
- **runtime.txt**: Python version specification
- **.env.example**: Template for environment variables
- **render.yaml**: Render deployment configuration
- **requirements.txt**: Python dependencies
- **.gitignore**: Git ignore rules

### Production Checklist

- [ ] DEBUG = False
- [ ] SECRET_KEY is unique and secure
- [ ] ALLOWED_HOSTS configured
- [ ] Static files collected
- [ ] Database configured (PostgreSQL recommended)
- [ ] Email configuration (if using email features)
- [ ] Logging configured
- [ ] Backups enabled
