# 🔍 OAuth Issue Diagnosis

## Problem Found

The OAuth callback is receiving **NO parameters**:
```json
{
  "all_params": [],
  "access_token": "missing",
  "refresh_token": "missing"
}
```

## Possible Causes

### 1. **GitHub Provider Not Enabled in Supabase** (Most Likely)

**Check:**
```
https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
```

Is GitHub:
- ❌ **Disabled** - This would cause Supabase to reject the OAuth flow
- ✅ **Enabled** - Good!

If disabled or missing credentials:
- Supabase redirects back without tokens
- You get empty callback

**Fix:**
1. Go to Supabase Auth Providers
2. Enable GitHub
3. Add Client ID + Client Secret from GitHub OAuth app

---

### 2. **Tokens in URL Hash Instead of Query Params**

Supabase might be using **implicit flow** (tokens in `#hash`) instead of **server flow** (tokens in `?query`).

**Test:**
Visit this test page and click GitHub button:
```
http://localhost:8000/test_callback.html
```

Then modify Supabase redirect to use this test page temporarily.

---

### 3. **PKCE Flow Enabled**

Supabase might be using PKCE (Proof Key for Code Exchange) which requires different handling.

---

## Quick Tests

### Test 1: Check what Supabase returns

**Manually trigger OAuth:**
```bash
# Visit this in browser:
https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/authorize?provider=github&redirect_to=http://localhost:8000/test_callback.html
```

Watch the URL after redirect - what parameters do you see?

---

### Test 2: Check Supabase Logs

1. Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/logs/auth-logs
2. Look for recent GitHub authentication attempts
3. Check for errors

---

### Test 3: Verify Callback Route

```bash
php artisan route:list | grep callback
```

Should show:
```
GET auth/callback ... supabase.callback
```

---

## Most Likely Solution

**GitHub is not configured in Supabase!**

### Complete Setup:

**Step 1: Create GitHub OAuth App**
1. Go to: https://github.com/settings/developers
2. New OAuth App
3. Settings:
   ```
   Name: Event Horizon
   Homepage: http://localhost:8000
   Callback: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
   ```
4. Save Client ID + Secret

**Step 2: Configure Supabase**
1. Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
2. Click GitHub
3. Enable it
4. Paste Client ID + Secret
5. **IMPORTANT:** Check "Redirect URLs" section
   - Should include: `http://localhost:8000/auth/callback`
6. Save

**Step 3: Test**
```bash
# Clear browser cache
# Visit in incognito mode
http://localhost:8000/login

# Click GitHub button
# Should redirect to GitHub
# Approve
# Should come back logged in
```

---

## Alternative: Check if Supabase is using Fragment/Hash

Supabase might be returning tokens like this:
```
http://localhost:8000/auth/callback#access_token=xxx&refresh_token=yyy
```

Instead of:
```
http://localhost:8000/auth/callback?access_token=xxx&refresh_token=yyy
```

If that's the case, we need to use JavaScript to extract from hash.

---

## Debug Commands

**Check what URL pattern Supabase generates:**
```bash
php artisan tinker
>>> $supabase = app(\App\Services\SupabaseService::class);
>>> $url = $supabase->getOAuthUrl('github', url('/auth/callback'));
>>> echo $url;
```

**Watch logs in real-time:**
```bash
tail -f storage/logs/laravel.log
```

**Check Supabase auth settings:**
```
https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/url-configuration
```

Look at:
- Redirect URLs
- Site URL
- OAuth flow type

---

## TL;DR - What to Do Now

1. **Go to Supabase Dashboard**
2. **Enable GitHub Provider**
3. **Add GitHub OAuth credentials**
4. **Try again**

If still fails:
- Check browser console
- Check Supabase auth logs
- Visit test_callback.html to see what parameters come back

---

Built with ❤️ for Event Horizon
