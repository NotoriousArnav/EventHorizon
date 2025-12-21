# Google OAuth Setup Guide

Quick guide for adding Google OAuth to Event Horizon (already configured, just needs credentials).

## Prerequisites

- ✅ Django app is deployed (Vercel/Railway/etc.)
- ✅ You have a Google account
- ✅ Google Provider already enabled in settings

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **Select a project** → **New Project**
3. Project name: **Event Horizon**
4. Click **Create**
5. Wait for project to be created (~30 seconds)

### 2. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. User Type: **External**
3. Click **Create**

#### App Information
```
App name: Event Horizon
User support email: your-email@example.com
App logo: (optional - upload your logo)
```

#### App Domain
```
Application home page: https://your-app.vercel.app
Application privacy policy: https://your-app.vercel.app/privacy (optional)
Application terms of service: https://your-app.vercel.app/terms (optional)
```

#### Authorized Domains
```
your-app.vercel.app
yourdomain.com (if you have custom domain)
```

#### Developer Contact
```
Email addresses: your-email@example.com
```

4. Click **Save and Continue**

#### Scopes
1. Click **Add or Remove Scopes**
2. Select:
   - ✅ `.../auth/userinfo.email` - View your email address
   - ✅ `.../auth/userinfo.profile` - See your personal info
   - ✅ `openid` - OpenID Connect
3. Click **Update**
4. Click **Save and Continue**

#### Test Users (Optional)
Add test users if app is in testing mode (not required for production):
- Click **Add Users**
- Add email addresses
- Click **Save and Continue**

5. Click **Back to Dashboard**

### 3. Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Application type: **Web application**
4. Name: **Event Horizon Web Client**

#### Authorized JavaScript Origins
```
Development:
http://localhost:8000
http://127.0.0.1:8000

Production:
https://your-app.vercel.app
https://yourdomain.com (if custom domain)
```

#### Authorized Redirect URIs
```
Development:
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/

Production:
https://your-app.vercel.app/accounts/google/login/callback/
https://yourdomain.com/accounts/google/login/callback/
```

5. Click **Create**

### 4. Copy Credentials

You'll see a dialog with:
- **Client ID**: `123456789-abcdefgh.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-xxxxxxxxxxxxxxxx`

**Copy both** - you'll need them!

### 5. Add to Django Admin (Development)

1. Start server: `uv run python manage.py runserver`
2. Go to: `http://127.0.0.1:8000/admin/`
3. Login with superuser
4. Go to: **Social Applications** → **Add Social Application**

Fill in:
```
Provider: Google
Name: Google
Client ID: [paste your Client ID]
Secret key: [paste your Client Secret]
Sites: Choose your site (example.com)
```

6. Click **Save**

### 6. Add to Production (Vercel)

#### Option A: Environment Variables
Add to Vercel Dashboard → Settings → Environment Variables:
```bash
GOOGLE_CLIENT_ID=123456789-abcdefgh.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxxxxxxxxxx
```

Then configure in Django admin on production.

#### Option B: Directly in Production Admin
1. Go to: `https://your-app.vercel.app/admin/`
2. Add social application (same as development steps)

### 7. Test Google Login

#### Development
1. Go to: `http://127.0.0.1:8000/accounts/login/`
2. Click **Continue with Google**
3. Select Google account
4. Authorize Event Horizon
5. Should redirect back and be logged in!

#### Production
1. Go to: `https://your-app.vercel.app/accounts/login/`
2. Click **Continue with Google**
3. Should work seamlessly!

## Publish Your App (Remove Testing Mode)

Once ready for production:

1. Go to **OAuth consent screen**
2. Click **Publish App**
3. Confirm you want to publish
4. Status changes to **In production**

**Note:** While in testing mode, only added test users can login. Publishing removes this restriction.

## Troubleshooting

### Error: "Redirect URI mismatch"

Check:
- URL exactly matches (including trailing slash)
- HTTPS in production (required)
- No typos
- Correct format: `/accounts/google/login/callback/`

### Error: "Access blocked: This app's request is invalid"

- OAuth consent screen not configured
- Missing required scopes
- App not published (and user not in test users)

### Error: "Social app for provider 'google' not found"

- Social application not added in Django admin
- Wrong site selected in social app
- Provider name incorrect (must be exactly "google")

## Verification Checklist

- [ ] Google Cloud project created
- [ ] OAuth consent screen configured
- [ ] OAuth credentials created
- [ ] Client ID and Secret copied
- [ ] Added to Django admin (dev)
- [ ] Added to production
- [ ] Tested login in development
- [ ] Tested login in production
- [ ] App published (for public access)

## Security Notes

- ✅ **Never commit secrets to Git**
- ✅ Use environment variables for production
- ✅ Regenerate secrets if exposed
- ✅ Only request necessary scopes (email, profile)
- ✅ Use HTTPS in production (required by Google)

## Additional Resources

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [django-allauth Google Provider Docs](https://docs.allauth.org/en/latest/socialaccount/providers/google.html)
- Event Horizon OAuth Guide: `docs/features/oauth.md`

**Google OAuth is now configured! Users can sign in with their Google account.** 🎉
