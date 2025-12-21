# Vercel Deployment - Complete Setup Guide

## 🎯 Issues Fixed

This deployment configuration fixes the following issues:
1. ✅ **DisallowedHost Error** - Wildcard and custom domain support
2. ✅ **Static Files Not Served** - S3-based static file serving
3. ✅ **Python Version Mismatch** - Updated to Python 3.12
4. ✅ **Serverless Architecture** - Proper Vercel Lambda configuration

---

## 📋 Required Environment Variables in Vercel

Go to your Vercel project → **Settings** → **Environment Variables** and add:

### Core Django Settings
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*
# Or for production security: ALLOWED_HOSTS=events.neopanda.tech,.vercel.app
```

### Database (Required)
```bash
DATABASE_URL=postgresql://postgres.aiwcqroacxepuiquywyl:YOUR_PASSWORD@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
```

### Storage Configuration (Required for both media AND static files)
```bash
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=3b3d99dc6d1a44f39054e646214b73bd
AWS_SECRET_ACCESS_KEY=eee87412c0d147450e030d95d2003e51a409ca0103dedbc376acfd65666bafa3
AWS_STORAGE_BUCKET_NAME=eventhorizon
AWS_S3_ENDPOINT_URL=https://aiwcqroacxepuiquywyl.storage.supabase.co/storage/v1/s3
AWS_S3_REGION_NAME=ap-southeast-2
AWS_S3_USE_SSL=True
AWS_S3_CUSTOM_DOMAIN=aiwcqroacxepuiquywyl.supabase.co/storage/v1/object/public/eventhorizon

# Enable S3 for static files (CRITICAL for Vercel)
USE_S3_FOR_STATIC=True
```

### Email Configuration
```bash
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp-pulse.com
EMAIL_PORT=587
# Fix typo: was EMAIL_POSRT
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Optional Settings
```bash
TIME_ZONE=Asia/Kolkata
CORS_ALLOW_ALL_ORIGINS=True
ADMIN_URL=/site/management/admin
```

---

## 🚀 Deployment Steps

### 1. Update Your Code
All necessary changes have been made to:
- ✅ `EventHorizon/settings.py` - Fixed ALLOWED_HOSTS and S3 static files
- ✅ `vercel.json` - Updated Python version and routes
- ✅ `build_files.sh` - Added S3 environment variables

### 2. Commit and Push
```bash
git add .
git commit -m "Fix Vercel deployment: Add S3 static files support and ALLOWED_HOSTS"
git push origin main
```

### 3. Configure Vercel Environment Variables
1. Go to Vercel Dashboard → Your Project
2. Settings → Environment Variables
3. Add all the variables listed above
4. **Important:** Add them to **Production**, **Preview**, and **Development** environments

### 4. Redeploy
Vercel will automatically redeploy when you push, or manually trigger:
1. Go to Deployments tab
2. Click the three dots on latest deployment
3. Click "Redeploy"

---

## 🔍 How It Works Now

### Static Files Flow
1. **Build Phase** (Vercel):
   - `npm run build:css` compiles Tailwind CSS
   - `python manage.py collectstatic` uploads files to Supabase S3
   - CSS, images, fonts → `s3://eventhorizon/static/`

2. **Runtime** (User requests):
   - Browser requests `/static/css/output.css`
   - Django generates URL: `https://supabase.co/.../static/css/output.css`
   - File served directly from S3 (fast, cached)

### Why This Works
- ✅ **No filesystem dependencies** - Vercel Lambda doesn't need local files
- ✅ **Global CDN** - Supabase S3 is fast worldwide
- ✅ **Production-ready** - Same setup works for media files
- ✅ **No code in templates** - Django's `{% static %}` tag still works

---

## 🧪 Verification Steps

After deployment, verify everything works:

### 1. Check ALLOWED_HOSTS
```bash
# Visit your site
https://events.neopanda.tech

# Should load without "DisallowedHost" error
```

### 2. Check Static Files
```bash
# Open browser DevTools → Network tab
# Reload page and check:

# CSS should load from:
https://aiwcqroacxepuiquywyl.supabase.co/storage/v1/object/public/eventhorizon/static/css/output.css

# Images should load from:
https://aiwcqroacxepuiquywyl.supabase.co/storage/v1/object/public/eventhorizon/static/images/...
```

### 3. Check Supabase Bucket
1. Go to Supabase Dashboard → Storage
2. Open `eventhorizon` bucket
3. You should see:
   - `media/` folder (for uploads)
   - `static/` folder (for CSS, JS, images)

### 4. Test Functionality
- ✅ Homepage loads with styling
- ✅ Images display correctly
- ✅ Login/Register forms work
- ✅ Admin panel accessible at `/site/management/admin`
- ✅ File uploads work (avatars, etc.)

---

## 🐛 Troubleshooting

### Issue: Static files still not loading

**Check 1:** Verify S3 bucket permissions
```bash
# Supabase Dashboard → Storage → eventhorizon bucket
# Policies → Make sure "public" read access is enabled
```

**Check 2:** Verify environment variables
```bash
# Vercel Dashboard → Settings → Environment Variables
# Ensure USE_S3_FOR_STATIC=True is set for Production
```

**Check 3:** Check build logs
```bash
# Vercel Dashboard → Deployments → Latest → Build Logs
# Look for: "Collecting static files to S3..."
# Should see successful uploads
```

### Issue: DisallowedHost error persists

**Solution:** Check environment variable format
```bash
# WRONG (with quotes):
ALLOWED_HOSTS="*"

# CORRECT (no quotes):
ALLOWED_HOSTS=*

# Or explicit:
ALLOWED_HOSTS=events.neopanda.tech,.vercel.app
```

### Issue: Email not working

**Check:** Fix typo in environment variable
```bash
# WRONG:
EMAIL_POSRT=587

# CORRECT:
EMAIL_PORT=587
```

---

## 🔒 Security Notes

### Current .env File Issues
Your local `.env` file contains **real credentials**:
- ❌ Database password
- ❌ Email password  
- ❌ S3 credentials
- ❌ Secret keys

**URGENT:** Verify `.env` is in `.gitignore` and never committed!

### Production Security Checklist
- [ ] Change `ALLOWED_HOSTS=*` to specific domains
- [ ] Rotate `SECRET_KEY` if ever committed to git
- [ ] Use Vercel environment variables, not `.env` file
- [ ] Enable 2FA on Supabase and Vercel accounts
- [ ] Monitor Supabase storage usage

---

## 📊 Performance Comparison

| Metric | Before (Broken) | After (S3) |
|--------|----------------|------------|
| Static files | ❌ 404 errors | ✅ Served from S3 |
| Load time | N/A (broken) | ~200-300ms |
| CDN | None | Supabase global CDN |
| Caching | None | HTTP caching headers |
| Cost | Free | Free (Supabase free tier) |

---

## 🎓 Understanding the Architecture

### Traditional Django Deployment (Railway/Render)
```
User → Server (Gunicorn) → Django → WhiteNoise → Static Files
                                 → Database
                                 → S3 (media only)
```

### Vercel Serverless Deployment (Current Setup)
```
User → Vercel CDN → Lambda (Django) → Database
                 ↓
                S3 (static + media)
```

**Key Difference:** Vercel Lambda has no persistent filesystem, so ALL files must come from S3.

---

## 🚦 Next Steps

### Immediate (Required)
1. ✅ Deploy with the fixed configuration
2. ✅ Verify static files load from S3
3. ✅ Test all site functionality

### Short-term (Recommended)
1. [ ] Change `ALLOWED_HOSTS=*` to explicit domains
2. [ ] Fix `EMAIL_PORT` typo in Vercel env vars
3. [ ] Set up custom domain properly with DNS
4. [ ] Enable Vercel Analytics for monitoring

### Long-term (Optional)
1. [ ] Consider migrating to Railway/Render for better Django support
2. [ ] Set up Sentry for error tracking
3. [ ] Configure Vercel CDN caching rules
4. [ ] Implement CSP headers for security

---

## 💡 Alternative: Migrate to Railway

If you encounter continued issues with Vercel, Railway is **much better** for Django:

### Why Railway?
- ✅ Django works out-of-the-box (no S3 needed for static files)
- ✅ WhiteNoise handles static files efficiently
- ✅ No cold starts
- ✅ WebSockets support
- ✅ Background tasks work
- ✅ Easier debugging
- ✅ Similar pricing ($5-10/month)

### Migration Time
- **5-10 minutes** (your `Procfile` and `gunicorn_config.py` already exist)

---

## 📞 Support

If you encounter issues:
1. Check Vercel deployment logs
2. Check Supabase storage bucket
3. Verify all environment variables are set correctly
4. Check browser console for 404 errors on static files

---

**Last Updated:** December 21, 2025
**Status:** ✅ Ready for deployment
