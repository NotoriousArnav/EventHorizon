# GitHub OAuth Debugging Guide 🐙🔧

## Common Issues & Fixes

### ✅ Issue #1: Wrong Callback URL (FIXED!)

**Problem:** OAuth was using `http://localhost/auth/callback` instead of `http://localhost:8000/auth/callback`

**Fix:** Updated `.env`:
```env
APP_URL=http://localhost:8000  # ✅ Now includes port
```

**Verify:**
```bash
php artisan config:clear
php artisan tinker --execute="dump(url('/auth/callback'));"
```
Should output: `http://localhost:8000/auth/callback`

---

### 🔍 Issue #2: GitHub Provider Not Enabled in Supabase

**Check:**
1. Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
2. Look for **GitHub** provider
3. Is it enabled? ✅ or ❌

**Fix if disabled:**
1. Click on GitHub
2. Enable it
3. You'll see it needs GitHub OAuth app credentials

---

### 🔑 Issue #3: GitHub OAuth App Not Configured

**Supabase needs GitHub OAuth credentials to work!**

#### Step-by-Step Setup:

**A. Create GitHub OAuth App:**
1. Go to: https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in:
   ```
   Application name: Event Horizon
   Homepage URL: http://localhost:8000
   Authorization callback URL: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
   ```
   
   ⚠️ **IMPORTANT:** The callback URL MUST be:
   ```
   https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
   ```
   NOT your Laravel app URL!

4. Click **"Register application"**
5. You'll get:
   - **Client ID**: `Ov23li...` (something like this)
   - **Client Secret**: Click "Generate a new client secret"

**B. Add to Supabase:**
1. Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
2. Click **GitHub**
3. Paste:
   - **Client ID** → GitHub Client ID field
   - **Client Secret** → GitHub Client Secret field
4. Click **Save**

---

### 🔄 OAuth Flow (What Should Happen)

```
User clicks GitHub button
    ↓
Laravel: /auth/oauth/github
    ↓
Redirects to: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/authorize?provider=github&redirect_to=http://localhost:8000/auth/callback
    ↓
Supabase redirects to: https://github.com/login/oauth/authorize?client_id=...
    ↓
User authorizes on GitHub
    ↓
GitHub redirects to: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback?code=...
    ↓
Supabase exchanges code for tokens
    ↓
Supabase redirects to: http://localhost:8000/auth/callback?access_token=...&refresh_token=...
    ↓
Laravel extracts tokens
    ↓
User logged in!
```

---

### 🧪 Test the OAuth Flow

**1. Test the OAuth redirect URL generation:**
```bash
php artisan tinker
>>> $supabase = app(\App\Services\SupabaseService::class);
>>> $url = $supabase->getOAuthUrl('github', url('/auth/callback'));
>>> dump($url);
```

Should output:
```
https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/authorize?provider=github&redirect_to=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Fcallback
```

**2. Visit the GitHub button manually:**
```bash
curl -I http://localhost:8000/auth/oauth/github
```

Should return a 302 redirect to Supabase.

**3. Check browser console:**
Open http://localhost:8000/login in browser
- Open DevTools (F12)
- Click GitHub button
- Watch Network tab for redirects

---

### 📋 Checklist

- [ ] `APP_URL=http://localhost:8000` in `.env`
- [ ] Config cache cleared: `php artisan config:clear`
- [ ] GitHub provider enabled in Supabase
- [ ] GitHub OAuth app created
- [ ] Callback URL in GitHub app: `https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback`
- [ ] Client ID & Secret added to Supabase
- [ ] Routes exist: `php artisan route:list | grep oauth`

---

### 🔍 Debugging Commands

**Check routes:**
```bash
php artisan route:list | grep oauth
```
Should show:
```
GET  auth/oauth/{provider}  - supabase.oauth
GET  auth/callback          - supabase.callback
```

**Check Supabase config:**
```bash
php artisan tinker --execute="dump(config('services.supabase'));"
```

**Test URL generation:**
```bash
php artisan tinker
>>> url('/auth/callback')
=> "http://localhost:8000/auth/callback"  // ✅ Should have :8000
```

**Check callback route:**
```bash
curl http://localhost:8000/auth/callback?access_token=test
```
Should redirect to login with error (since token is fake)

---

### ⚠️ Common Errors

**Error: "redirect_uri mismatch"**
- GitHub OAuth app callback URL is wrong
- Must be: `https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback`
- NOT: `http://localhost:8000/auth/callback`

**Error: "Provider not found"**
- GitHub provider not enabled in Supabase
- Go enable it in Supabase Dashboard

**Error: "Invalid client_id"**
- Client ID not configured in Supabase
- Or wrong Client ID entered

**Error: Page keeps loading**
- Check browser console for errors
- Check if redirect_to URL is correct
- Verify APP_URL in .env

**Error: "OAuth login failed"**
- Token not found in callback URL
- Check Supabase logs
- Verify GitHub app is active

---

### 📸 What Success Looks Like

**1. Click GitHub button:**
- Redirects to GitHub
- URL shows: `github.com/login/oauth/authorize?client_id=...`

**2. Authorize on GitHub:**
- Shows "Event Horizon wants to access..."
- Click "Authorize"

**3. Redirected back:**
- URL briefly shows: `localhost:8000/auth/callback?access_token=...`
- Then redirects to: `localhost:8000/dashboard`
- You're logged in!

**4. Check Supabase:**
- Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/users
- Your GitHub account should be listed

---

### 🆘 Still Not Working?

**Enable debug logging:**

Add to `app/Http/Controllers/Auth/SupabaseAuthController.php`:

```php
public function oauthCallback(Request $request)
{
    // Add debug logging
    \Log::info('OAuth callback received', [
        'access_token' => $request->query('access_token') ? 'present' : 'missing',
        'refresh_token' => $request->query('refresh_token') ? 'present' : 'missing',
        'all_params' => $request->all()
    ]);

    $accessToken = $request->query('access_token');
    // ... rest of code
}
```

Then check logs:
```bash
tail -f storage/logs/laravel.log
```

Click GitHub button and watch what parameters come back.

---

### 💡 Quick Fix Checklist

If GitHub OAuth fails, try these in order:

1. **Clear Laravel config:**
   ```bash
   php artisan config:clear
   ```

2. **Verify APP_URL:**
   ```bash
   grep APP_URL .env
   # Should be: APP_URL=http://localhost:8000
   ```

3. **Check Supabase GitHub is enabled:**
   https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers

4. **Verify GitHub OAuth app callback URL:**
   ```
   https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
   ```

5. **Test in browser incognito:**
   Sometimes cached redirects cause issues

---

### 🎯 TL;DR - Most Likely Issue

**You probably need to:**

1. **Enable GitHub in Supabase Dashboard**
2. **Create GitHub OAuth App** with callback: `https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback`
3. **Add credentials to Supabase**

That's 90% of GitHub OAuth issues! ✅

---

Built with ❤️ for Event Horizon
