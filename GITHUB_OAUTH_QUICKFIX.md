# GitHub OAuth Quick Fix Guide 🚀

## ✅ FIXED: APP_URL Issue
Changed `.env` from:
```env
APP_URL=http://localhost     ❌ Missing port
```

To:
```env
APP_URL=http://localhost:8000  ✅ Correct
```

**Cleared config cache** - URLs now generate correctly!

---

## 🔧 Most Likely Remaining Issue

**GitHub provider is probably not configured in Supabase yet!**

### Quick 3-Step Fix:

#### **Step 1: Create GitHub OAuth App**
1. Go to: https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in:
   - **Application name**: Event Horizon
   - **Homepage URL**: http://localhost:8000
   - **Authorization callback URL**: 
     ```
     https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/callback
     ```
     ⚠️ Use the Supabase URL, NOT localhost!

4. Click **"Register application"**
5. Save the **Client ID**
6. Click **"Generate a new client secret"** and save it

#### **Step 2: Configure in Supabase**
1. Go to: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers
2. Find **GitHub** and click it
3. **Enable** the provider
4. Paste:
   - Your GitHub **Client ID**
   - Your GitHub **Client Secret**
5. Click **Save**

#### **Step 3: Test It**
1. Visit: http://localhost:8000/login
2. Click the **GitHub** button
3. Should redirect to GitHub for authorization
4. After approving, you'll be logged in!

---

## 🔍 Debug Logging Added

Now when OAuth callback happens, it logs everything to help debug:

```bash
# Watch the logs in real-time:
tail -f storage/logs/laravel.log
```

When you click GitHub button, you'll see:
- What parameters Supabase sends back
- If access_token is present
- Any errors that occur

---

## 📊 Current Status

✅ **Fixed:**
- APP_URL now includes port `:8000`
- OAuth redirect URLs generate correctly
- Debug logging added

❓ **Needs Configuration:**
- GitHub OAuth app (create in GitHub)
- GitHub provider in Supabase (enable + add credentials)

---

## 🧪 Test Your Setup

**1. Check OAuth URL generation:**
```bash
curl -I http://localhost:8000/auth/oauth/github
```

Should show redirect to:
```
Location: https://aiwcqroacxepuiquywyl.supabase.co/auth/v1/authorize?provider=github&redirect_to=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Fcallback
```

**2. Check if GitHub is enabled in Supabase:**
Visit: https://app.supabase.com/project/aiwcqroacxepuiquywyl/auth/providers

Look for GitHub - is it enabled? ✅ or ❌

---

## 💡 TL;DR

**The app code is correct!** 

You just need to:
1. **Create GitHub OAuth app** (5 minutes)
2. **Enable GitHub in Supabase** (2 minutes)
3. **Test it** (30 seconds)

Total: ~7 minutes to working GitHub OAuth! 🎉

---

**See `GITHUB_OAUTH_DEBUG.md` for detailed troubleshooting.**

Built with ❤️ for Event Horizon
