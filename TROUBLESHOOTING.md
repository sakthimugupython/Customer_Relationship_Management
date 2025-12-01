## 🛠️ Troubleshooting Guide for Render Deployment

### Problem: CSS/JavaScript Not Loading on Render

**Solution:**
```python
# Verify settings.py has:
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Steps to fix:**
1. SSH into Render instance
2. Run: `python manage.py collectstatic --clear --noinput`
3. Restart the service
4. Clear browser cache (Ctrl+Shift+Delete)

---

### Problem: Images/Icons Not Displaying

**Cause:** Bootstrap Icons CDN or static files not collected

**Solution:**
```bash
# Local testing
python manage.py collectstatic --noinput
python manage.py runserver

# Check staticfiles directory is created
ls -la staticfiles/
```

---

### Problem: 500 Error on Login

**Check logs:**
1. Go to Render Dashboard → Logs
2. Look for Django errors
3. Ensure DEBUG=False doesn't hide real errors locally

**Common causes:**
- SECRET_KEY not set in environment
- Database connection error
- Missing migrations

**Fix:**
```bash
# SSH into Render
python manage.py migrate
python manage.py createsuperuser
```

---

### Problem: Static Files Work Locally but Not on Render

**Verify:**
- [ ] Procfile exists in root directory
- [ ] WhiteNoiseMiddleware in MIDDLEWARE list
- [ ] STATIC_ROOT and STATIC_URL configured
- [ ] Build command includes `collectstatic --noinput`
- [ ] requirements.txt includes whitenoise

**Debug:**
```python
# Add to settings.py temporarily
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Run locally
python manage.py collectstatic --noinput --verbosity 3
```

---

### Problem: "No Such Module 'whitenoise'"

**Fix:**
```bash
pip install whitenoise
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add whitenoise"
git push origin main
# Redeploy on Render
```

---

### Problem: Database Connection Error

**If using SQLite (not recommended):**
- Works locally but fails on Render
- Use PostgreSQL instead

**To set up PostgreSQL:**
1. Create PostgreSQL database on Render
2. Copy connection string
3. Set DATABASE_URL in environment variables
4. Render will automatically use it

---

### Problem: Admin Panel Not Working

**Steps:**
1. SSH into Render
2. Run: `python manage.py createsuperuser`
3. Follow prompts to create admin account
4. Access at: `https://yourapp.onrender.com/admin/`

---

### Problem: Changes Not Appearing After Deploy

**Solution:**
1. Clear Render cache
2. Force rebuild: Push to GitHub
3. Clear browser cache: Ctrl+Shift+Delete
4. Hard refresh: Ctrl+F5 (or Cmd+Shift+R on Mac)

---

### Problem: CSRF Token Errors

**Cause:** DEBUG=False with incorrect settings

**Fix in settings.py:**
```python
CSRF_COOKIE_SECURE = True if not DEBUG else False
SESSION_COOKIE_SECURE = True if not DEBUG else False
```

---

### Problem: Migrations Not Running

**Check Procfile:**
```
web: gunicorn crm_management.wsgi --log-file -
release: python manage.py migrate  # This line required
```

**Manual fix:**
1. SSH into Render
2. Run: `python manage.py migrate`
3. Restart service

---

### Quick Diagnostic Commands

**SSH into Render:**
```bash
# Check Python version
python --version

# Check static files
ls staticfiles/

# Check environment variables
env | grep DEBUG
env | grep SECRET_KEY

# Run Django check
python manage.py check

# Test database
python manage.py dbshell

# Check migrations
python manage.py showmigrations
```

---

### Common Environment Variable Issues

**Problem:** DEBUG not changing behavior

**Fix:** Restart service after setting DEBUG=False

**Check:**
```python
# In Django shell
python manage.py shell
>>> from django.conf import settings
>>> settings.DEBUG
# Should show False on production
```

---

### Performance Issues

**If page loads slowly:**
1. Check if static files are cached
2. Verify WhiteNoise compression working
3. Check database queries (Django debug toolbar locally)
4. Consider upgrading Render plan

**To verify static file compression:**
```
curl -I https://yourapp.onrender.com/static/...
# Look for: Content-Encoding: gzip
```

---

### Rollback to Previous Version

If deployment breaks:
```bash
git log --oneline
git revert <commit-hash>
git push origin main
# Render will auto-redeploy
```

---

### Contact Support

**Render Support:**
- https://render.com/support
- Email: support@render.com

**Django Issues:**
- https://docs.djangoproject.com/
- Stack Overflow tag: django

**WhiteNoise Issues:**
- https://whitenoise.readthedocs.io/

---

## ✅ Quick Checklist When Deployment Fails

- [ ] Check Render logs (Dashboard → Logs)
- [ ] Verify all files pushed to GitHub
- [ ] Check environment variables are set
- [ ] Ensure Procfile exists and is correct
- [ ] Run `python manage.py check` locally
- [ ] Test `collectstatic --noinput` locally
- [ ] Verify requirements.txt has all packages
- [ ] Clear browser cache
- [ ] Try hard refresh (Ctrl+Shift+R)
- [ ] Restart Render service
- [ ] Check for syntax errors in settings.py

---

**Still having issues?** Review DEPLOYMENT.md and RENDER_SETUP.md for detailed setup instructions!
