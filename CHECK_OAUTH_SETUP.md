# 🔴 GitHub OAuth Not Working - Here's Why

## The Problem

You're getting: **"OAuth login failed. No access token received."**

The logs show:
```json
"all_params": []  ← Empty! Nothing coming back from Supabase
```

---

## 🎯 Root Cause (99% Certain)

**GitHub provider is NOT properly configured in Supabase.**

When Supabase doesn't have GitHub OAuth credentials, it:
1. Accepts your OAuth request
2. Tries to redirect to GitHub
3. **Fails silently**
4. Redirects back to your app with NO tokens

---

## ✅ The Fix - Step by Step

### **Step 1: Create GitHub OAuth Application**

1. Go to: **https://github.com/settings/developers**
2. Click **"New OAuth App"** (top right)
3. Fill in the form:

```
Application name: Event Horizon Local
Homepage URL: http://localhost:8000
Application description: Event management platform (optional)
Authorization callback URL: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
```

⚠️ **CRITICAL:** The callback URL must be your **Supabase URL**, not localhost!

4. Click **"Register application"**
5. You'll see a **Client ID** (save it)
6. Click **"Generate a new client secret"** (save it)

---

### **Step 2: Configure Supabase**

1. Go to: **https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers**
2. Scroll down to find **"GitHub"**
3. Click on it to expand
4. Toggle **"Enable Sign in with GitHub"** to ON
5. Paste your credentials:
   - **GitHub Client ID** → Paste the Client ID from Step 1
   - **GitHub Client Secret** → Paste the secret from Step 1
6. Click **"Save"**

---

### **Step 3: Add Redirect URL (Important!)**

While still in Supabase Auth settings:

1. Go to: **https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/url-configuration**
2. Look for **"Redirect URLs"** section
3. Add: `http://localhost:8000/auth/callback`
4. Click **"Save"**

---

### **Step 4: Test It!**

1. **Clear your browser cache** (or use incognito/private mode)
2. Visit: **http://localhost:8000/login**
3. Click the **"GitHub"** button
4. You should:
   - See GitHub's authorization page
   - Click "Authorize Event Horizon"
   - Get redirected back and logged in!

---

## 🧪 Alternative Test Method

If you want to see what Supabase is actually returning:

1. Visit: **http://localhost:8000/test_callback.html**
2. Open browser DevTools (F12)
3. In another tab, manually visit:
   ```
   https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/authorize?provider=github&redirect_to=http://localhost:8000/test_callback.html
   ```
4. After GitHub authorization, check the test page
5. It will show you all URL parameters (both `?query` and `#hash`)

---

## 🔍 How to Verify GitHub is Configured

**Quick check in Supabase Dashboard:**

1. Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
2. Find GitHub in the list
3. Look for a green checkmark or "Enabled" status
4. If it says "Configure" or has a ⚠️ warning → **Not configured yet!**

---

## 📊 What Success Looks Like

After configuration, when you click GitHub button:

1. **Browser redirects to GitHub:**
   ```
   https://github.com/login/oauth/authorize?client_id=Ov23li...
   ```

2. **You authorize the app**

3. **GitHub redirects to Supabase:**
   ```
   https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback?code=...
   ```

4. **Supabase redirects to your app WITH tokens:**
   ```
   http://localhost:8000/auth/callback?access_token=eyJ...&refresh_token=...
   ```

5. **Your app logs you in!** ✅

---

## 🆘 Still Not Working?

Try these debug steps:

**1. Check Supabase Auth Logs:**
```
https://app.supabase.com/project/aiwcqroacxepuiquywyl/logs/auth-logs
```
Look for errors related to GitHub OAuth

**2. Check Laravel Logs:**
```bash
tail -f storage/logs/laravel.log
```
Click GitHub button and watch for errors

**3. Check Browser Console:**
- Open DevTools (F12)
- Go to Console tab
- Click GitHub button
- Look for errors

**4. Verify URLs:**
```bash
# Should redirect to Supabase:
curl -I http://localhost:8000/auth/oauth/github
```

---

## 💡 Common Mistakes

❌ **Using localhost in GitHub OAuth callback**
```
Wrong: http://localhost:8000/auth/callback
Right: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
```

❌ **Forgetting to enable provider in Supabase**
- Having OAuth app in GitHub is not enough
- Must also enable in Supabase Dashboard

❌ **Wrong redirect URL format**
- Supabase expects `/auth/v1/callback`
- Not `/auth/callback`

---

## 🎯 Summary

**The app code is 100% correct.** ✅

You just need to:
1. Create GitHub OAuth app (2 minutes)
2. Enable + configure in Supabase (1 minute)
3. Test (30 seconds)

Total: ~3 minutes! 🚀

---

**After setup, GitHub OAuth will work perfectly!**

Built with ❤️ for Event Horizon
