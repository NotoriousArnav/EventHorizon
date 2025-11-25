# Supabase Setup Guide for Event Horizon 🚀

## Your Project Details
- **Project ID:** `aiwcqroacxepuiquywyl`
- **Project URL:** `https://aiwcqroacxepuiquywyl.supabase.co`

---

## Step 1: Get Your API Keys

### Go to Supabase Dashboard:
```
https://app.supabase.com/project/aiwcqroacxepuiquywyl/settings/api
```

### You'll see a page with these sections:

#### 📍 **Project URL**
```
https://aiwcqroacxepuiquywyl.supabase.co
```
→ Copy this URL

#### 🔑 **Project API keys**

**anon / public key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOi...
```
→ Copy this key (it's a long JWT token)
→ This key is SAFE to use in frontend code

**service_role key:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOi...
```
→ **DO NOT USE** this for authentication (admin only)
→ Only use this for server-side admin operations

#### 🔐 **JWT Settings**

**JWT Secret:**
```
A long secret string (not a JWT)
```
→ Copy this secret
→ Keep this PRIVATE (never expose in frontend)

---

## Step 2: Update Your `.env` File

Add these lines to your `.env`:

```env
# Supabase Configuration
SUPABASE_URL=https://aiwcqroacxepuiquywyl.supabase.co
SUPABASE_ANON_KEY=paste-your-anon-key-here
SUPABASE_JWT_SECRET=paste-your-jwt-secret-here
```

### Example with placeholder keys:
```env
# Supabase Configuration
SUPABASE_URL=https://aiwcqroacxepuiquywyl.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFpd2Nxcm9hY3hlcHVpcXV5d3lsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2MTM1MjE1NTAsImV4cCI6MTkyOTA5NzU1MH0.example
SUPABASE_JWT_SECRET=your-very-long-secret-string-here
```

---

## Step 3: Configure Database Connection (PostgreSQL)

### Get Database Credentials:
```
https://app.supabase.com/project/aiwcqroacxepuiquywyl/settings/database
```

### Add to your `.env`:
```env
# Database Configuration (Supabase PostgreSQL)
DB_CONNECTION=pgsql
DB_HOST=db.aiwcqroacxepuiquywyl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=your-database-password-here
```

**Note:** The database password is shown when you first create the project. If you forgot it, you can reset it in the database settings.

---

## Step 4: Test Your Configuration

### Run this command:
```bash
php artisan tinker
```

### Then test Supabase connection:
```php
$supabase = app(\App\Services\SupabaseService::class);
dd(config('services.supabase'));
```

You should see:
```php
array:3 [
  "url" => "https://aiwcqroacxepuiquywyl.supabase.co"
  "key" => "eyJhbGci..."
  "jwt_secret" => "your-secret..."
]
```

---

## Step 5: Enable OAuth Providers (Optional)

### For Google OAuth:

1. **Go to Supabase Dashboard:**
   ```
   https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
   ```

2. **Find "Google" and click to enable**

3. **You'll need Google OAuth credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create OAuth 2.0 Client ID
   - Set Authorized redirect URI to:
     ```
     https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
     ```
   - Copy Client ID and Client Secret

4. **Paste in Supabase:**
   - Client ID → Google Client ID field
   - Client Secret → Google Client Secret field
   - Click Save

5. **Test OAuth:**
   - Visit `http://localhost:8000/login`
   - Click "Continue with Google"
   - Should redirect to Google consent screen

### For GitHub OAuth:

1. **Go to [GitHub Settings](https://github.com/settings/developers)**
2. **New OAuth App**
3. **Set Authorization callback URL to:**
   ```
   https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
   ```
4. **Copy Client ID and Client Secret**
5. **Enable GitHub in Supabase** and paste credentials

---

## Complete `.env` Example

```env
APP_NAME="Event Horizon"
APP_ENV=local
APP_KEY=base64:your-app-key-here
APP_DEBUG=true
APP_URL=http://localhost:8000

# Supabase Configuration
SUPABASE_URL=https://aiwcqroacxepuiquywyl.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-actual-key-here
SUPABASE_JWT_SECRET=your-jwt-secret-here

# Database Configuration (Supabase PostgreSQL)
DB_CONNECTION=pgsql
DB_HOST=db.aiwcqroacxepuiquywyl.supabase.co
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=postgres
DB_PASSWORD=your-database-password

# Session Configuration
SESSION_DRIVER=database
SESSION_LIFETIME=120

# Other Laravel configs...
```

---

## Quick Reference Links

| What | URL |
|------|-----|
| **API Keys** | https://app.supabase.com/project/aiwcqroacxepuiquywyl/settings/api |
| **Database Settings** | https://app.supabase.com/project/aiwcqroacxepuiquywyl/settings/database |
| **Auth Providers** | https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers |
| **Table Editor** | https://app.supabase.com/project/aiwcqroacxepuiquywyl/editor |
| **SQL Editor** | https://app.supabase.com/project/aiwcqroacxepuiquywyl/sql |
| **Auth Users** | https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/users |

---

## Testing Checklist

- [ ] Supabase URL configured in `.env`
- [ ] Anon key configured in `.env`
- [ ] JWT secret configured in `.env`
- [ ] Database credentials configured
- [ ] Run `php artisan config:clear`
- [ ] Visit `/register` - page loads
- [ ] Create test account
- [ ] Visit `/login` - page loads
- [ ] Login with test account
- [ ] Get redirected to `/dashboard`
- [ ] Session contains `supabase_access_token`
- [ ] Logout works
- [ ] OAuth providers enabled (optional)

---

## Troubleshooting

### "Invalid JWT" errors
- Check your `SUPABASE_JWT_SECRET` is correct
- Clear config cache: `php artisan config:clear`

### Can't connect to database
- Verify database password
- Check if IP is allowed (Supabase allows all by default)
- Confirm database host: `db.aiwcqroacxepuiquywyl.supabase.co`

### OAuth not working
- Verify redirect URI matches exactly
- Enable provider in Supabase dashboard
- Check OAuth app credentials

### Session not persisting
- Check `SESSION_DRIVER=database` in `.env`
- Run migrations: `php artisan migrate`
- Clear cache: `php artisan cache:clear`

---

## Security Notes

✅ **Safe to expose:**
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY` (designed for frontend use)

❌ **Keep secret:**
- `SUPABASE_JWT_SECRET`
- `SUPABASE_SERVICE_ROLE_KEY`
- `DB_PASSWORD`

---

Built with ❤️ for Event Horizon
