# Vercel Deployment Setup Guide

## ⚠️ Important: Vercel Limitations for Django

Vercel runs Django as **serverless functions**, which has significant limitations:
- ❌ No persistent file storage (use S3/Supabase for media files)
- ❌ No SQLite (must use PostgreSQL/MySQL)
- ❌ No WebSockets
- ❌ Cold start delays
- ❌ Each request is isolated

**Recommendation:** Consider using **Railway** or **Render** instead - they're much better suited for Django applications. See `DEPLOYMENT.md` for guides.

## Required Environment Variables

Set these in your Vercel project dashboard (Settings → Environment Variables):

### Core Django Settings
```bash
SECRET_KEY=your-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=.vercel.app,yourdomain.com
DJANGO_SETTINGS_MODULE=EventHorizon.settings
```

### Database (Required - Must be external)
```bash
# Option 1: Supabase PostgreSQL (Recommended)
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

# Option 2: Railway PostgreSQL
DATABASE_URL=postgresql://user:pass@containers-us-west-xxx.railway.app:5432/railway

# Option 3: Neon/PlanetScale/Any PostgreSQL
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Storage (Required for media files)
```bash
# Supabase Storage (Recommended)
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=sbxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=your-supabase-secret-key
AWS_STORAGE_BUCKET_NAME=eventhorizon
AWS_S3_ENDPOINT_URL=https://xxxxx.supabase.co/storage/v1/s3
AWS_S3_CUSTOM_DOMAIN=xxxxx.supabase.co/storage/v1/object/public/eventhorizon
AWS_S3_REGION_NAME=us-east-1
AWS_S3_USE_SSL=True
```

### Email (Optional but recommended)
```bash
# Gmail SMTP
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### OAuth (Optional)
```bash
# GitHub OAuth
GITHUB_CLIENT_ID=Ov23lixxxxxxxxx
GITHUB_CLIENT_SECRET=your-github-secret

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-secret
```

## Deployment Steps

### 1. Fork/Clone Repository
```bash
git clone https://github.com/NotoriousArnav/EventHorizon.git
cd EventHorizon
```

### 2. Setup Supabase (Required)

#### Database
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Create a new project
3. Wait for database to provision
4. Go to Settings → Database → Connection String
5. Copy the connection string (URI format)
6. Add to Vercel as `DATABASE_URL`

#### Storage
1. In Supabase Dashboard → Storage
2. Create a bucket named `eventhorizon`
3. Make it public (or configure RLS policies)
4. Go to Settings → API
5. Get your S3 credentials:
   - Access Key ID (starts with `sb`)
   - Secret Access Key
   - Endpoint URL: `https://[project-ref].supabase.co/storage/v1/s3`
6. Add all storage variables to Vercel

### 3. Deploy to Vercel

#### Option A: Via GitHub (Recommended)
1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Add New" → "Project"
4. Import your GitHub repository
5. Configure:
   - Framework Preset: **Other**
   - Build Command: (leave empty, uses vercel.json)
   - Output Directory: (leave empty)
6. Add all environment variables (see above)
7. Click "Deploy"

#### Option B: Via Vercel CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

### 4. Run Database Migrations

After first deployment, you need to run migrations. SSH into Vercel or use this workaround:

Create a temporary management command endpoint (⚠️ remove after use!):

```python
# Add to EventHorizon/urls.py for one-time setup
from django.core.management import call_command
from django.http import HttpResponse

def run_migrations(request):
    if request.GET.get('secret') == 'your-secret-token':
        call_command('migrate')
        return HttpResponse('Migrations complete')
    return HttpResponse('Unauthorized', status=401)

# Add to urlpatterns temporarily
path('admin/migrations/', run_migrations),
```

Visit: `https://your-app.vercel.app/admin/migrations/?secret=your-secret-token`

**Remove this endpoint immediately after use!**

### 5. Create Superuser

Option 1: Use Django shell (if Vercel supports it):
```bash
vercel env pull
python manage.py createsuperuser
```

Option 2: Create via database:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'password')
```

### 6. Configure OAuth Callbacks (If using)

#### GitHub OAuth
- Application callback URL: `https://your-app.vercel.app/accounts/github/login/callback/`

#### Google OAuth
- Authorized redirect URIs: `https://your-app.vercel.app/accounts/google/login/callback/`

Add credentials to Django admin: `/admin/socialaccount/socialapp/`

## Troubleshooting

### Static Files Not Loading
- ✅ WhiteNoise is already configured
- ✅ output.css is now tracked in git
- Run `python manage.py collectstatic --noinput` locally and verify files

### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Ensure database allows external connections
- Check SSL requirements (Supabase requires SSL)

### Import Errors
- Vercel Python runtime has limited packages
- Heavy ML libraries may not work
- Check `requirements.txt` is complete

### Cold Starts
- First request after inactivity is slow (5-10s)
- Use Vercel Pro for better performance
- Consider Railway/Render for always-on instances

### Media Files Not Saving
- Local file storage doesn't work on Vercel
- Must use S3/Supabase Storage
- Verify `STORAGE_BACKEND=s3` is set

## Alternative: Use Railway (Recommended)

Railway is much better for Django:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up

# Add PostgreSQL
railway add postgres

# Set environment variables
railway variables set SECRET_KEY=your-key
railway variables set ALLOWED_HOSTS=.railway.app

# Deploy
railway up
```

See `DEPLOYMENT.md` for complete Railway setup guide.

## Alternative: Use Render

Render also has excellent Django support:

1. Connect GitHub repository
2. Select "Web Service"
3. Build Command: `./build.sh`
4. Start Command: `gunicorn EventHorizon.wsgi:application`
5. Add PostgreSQL database (free tier available)
6. Add environment variables

See `DEPLOYMENT.md` for complete Render setup guide.

## Status Check

After deployment, verify:
- [ ] Homepage loads at `https://your-app.vercel.app`
- [ ] Static files load (CSS, images)
- [ ] Admin panel works `/admin/`
- [ ] Can login with superuser
- [ ] Database queries work
- [ ] Media uploads work (avatar upload test)
- [ ] Email verification sends (if configured)
- [ ] OAuth login works (if configured)

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **Supabase Docs**: https://supabase.com/docs
- **Project Issues**: https://github.com/NotoriousArnav/EventHorizon/issues

## Notes

- Vercel has a **10MB** function size limit - our app is configured for 15MB but may need optimization
- Free tier has usage limits - monitor your dashboard
- For production, consider:
  - Vercel Pro ($20/month) for better limits
  - Railway ($5/month) for PostgreSQL + app
  - Render (Free tier for small apps)
  
**The 10x fun continues even on serverless!** 🚀
