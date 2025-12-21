# UptimeRobot Setup Guide

Prevent cold starts and monitor your Event Horizon deployment with UptimeRobot.

## What is UptimeRobot?

UptimeRobot is a free uptime monitoring service that:
- ✅ Pings your website every 5 minutes (free tier)
- ✅ Prevents serverless cold starts by keeping your app warm
- ✅ Alerts you if your site goes down
- ✅ Provides uptime statistics and reports
- ✅ Completely free for up to 50 monitors

**Perfect for Vercel deployments!**

---

## Why You Need This for Vercel

### The Cold Start Problem

Vercel serverless functions "sleep" after inactivity:
- ⏱️ First request after sleep: **5-15 seconds** (cold start)
- ⚡ Subsequent requests: **~100ms** (warm)
- 😴 Goes cold after: **~5-10 minutes** of inactivity

### The Solution

UptimeRobot pings your site every 5 minutes, keeping it warm 24/7!

- ✅ No more slow first-page loads
- ✅ Better user experience
- ✅ Consistent response times
- ✅ Database connections stay active

---

## Setup Instructions

### 1. Create UptimeRobot Account

1. Go to [UptimeRobot](https://uptimerobot.com/)
2. Click **Sign Up Free**
3. Create account (email + password or Google sign-in)
4. Verify your email

### 2. Add Your First Monitor

#### Basic Monitor (Recommended)
1. Click **+ Add New Monitor**
2. Configure:

```
Monitor Type: HTTP(s)
Friendly Name: Event Horizon (Production)
URL (or IP): https://event-horizon-27b1u7uk2-notoriousarnavs-projects.vercel.app
Monitoring Interval: 5 minutes (free tier)
Monitor Timeout: 30 seconds
```

3. Click **Create Monitor**

#### Advanced Options (Optional)

**HTTP Method:**
- Use **HEAD** instead of GET (faster, uses less bandwidth)
- Or use **GET** for more realistic monitoring

**Keyword Monitoring:**
- Enable: **Keyword Exists**
- Add keyword: `Event Horizon` (check if page content loads correctly)
- Case sensitive: No

**Custom HTTP Headers:**
```
User-Agent: UptimeRobot/2.0
```

### 3. Add Multiple Endpoints

To keep different parts of your app warm:

#### Homepage
```
Name: Event Horizon - Homepage
URL: https://your-app.vercel.app/
```

#### API Health Check
```
Name: Event Horizon - API
URL: https://your-app.vercel.app/api/v1/events/
```

#### Admin Panel
```
Name: Event Horizon - Admin
URL: https://your-app.vercel.app/admin/
```

**Tip:** Use different intervals (5, 7, 10 minutes) to distribute load.

### 4. Setup Alert Contacts

Get notified when your site goes down:

1. Go to **My Settings** → **Alert Contacts**
2. Add email notification:
   - Email: Your email
   - Verify the email
3. Add more contacts (optional):
   - Slack webhook
   - Discord webhook
   - SMS (paid feature)
   - Telegram bot

### 5. Configure Notifications

For each monitor:
1. Click monitor → **Edit**
2. Scroll to **Alert Contacts to Notify**
3. Select your email/contacts
4. Configure alerts:
   - ✅ When monitor goes down
   - ✅ When monitor goes back up
   - ✅ Get notified every time down is detected (or just once)

---

## Optimal Configuration for Vercel

### Recommended Setup

**Monitor 1: Homepage (Keep Warm)**
```
URL: https://your-app.vercel.app/
Method: HEAD
Interval: 5 minutes
Alerts: Enabled
```

**Monitor 2: Health Check (Verify Functionality)**
```
URL: https://your-app.vercel.app/api/v1/events/
Method: GET
Interval: 10 minutes
Keyword: "results" or "count"
Alerts: Enabled
```

### Why This Works

- Homepage ping every 5 minutes keeps serverless functions warm
- API check every 10 minutes verifies database connectivity
- Different intervals prevent spamming Vercel
- HEAD requests are lighter than GET

---

## Create a Health Check Endpoint (Optional)

For better monitoring, create a dedicated health check endpoint:

### 1. Create Health Check View

Add to `home/views.py`:

```python
from django.http import JsonResponse
from django.db import connection
import datetime

def health_check(request):
    """Health check endpoint for monitoring services"""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            "status": "healthy",
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "database": "connected",
            "service": "Event Horizon"
        })
    except Exception as e:
        return JsonResponse({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }, status=503)
```

### 2. Add URL Route

Add to `home/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("health/", views.health_check, name="health_check"),
]
```

### 3. Update UptimeRobot Monitor

```
URL: https://your-app.vercel.app/health/
Method: GET
Keyword: "healthy"
Interval: 5 minutes
```

Now UptimeRobot will:
- ✅ Keep your app warm
- ✅ Verify database is working
- ✅ Alert if anything breaks

---

## Monitor Multiple Deployments

If you have staging/preview deployments:

### Production
```
Name: Event Horizon (Production)
URL: https://eventhorizon.vercel.app
Interval: 5 minutes
```

### Preview/Staging
```
Name: Event Horizon (Staging)
URL: https://event-horizon-git-dev-username.vercel.app
Interval: 15 minutes (less frequent)
```

### Custom Domain
```
Name: Event Horizon (Custom Domain)
URL: https://yourdomain.com
Interval: 5 minutes
```

---

## Advanced: Distributed Monitoring

UptimeRobot Pro features (paid):
- 📍 Monitor from multiple locations
- ⏱️ Check every 1 minute (vs 5 minutes free)
- 📊 Advanced statistics
- 🔔 SMS alerts
- 📱 Mobile app

**Free tier is usually enough for most apps!**

---

## Monitoring Dashboard

### View Statistics

1. Go to **Dashboard**
2. See all monitors at a glance:
   - 🟢 Up: Site is responding
   - 🔴 Down: Site is offline
   - 🟡 Seems down: Investigating
   - ⚪ Paused: Monitor disabled

### Response Time Graph

Click any monitor to see:
- Average response time
- Uptime percentage (aim for 99%+)
- Downtime incidents
- Response time trends

### Public Status Page (Optional)

Create a public status page:
1. Go to **Public Status Pages**
2. Click **+ Add New PSP**
3. Select monitors to include
4. Customize design
5. Get public URL: `https://stats.uptimerobot.com/YOUR_ID`

Share with users to show real-time status!

---

## Best Practices

### DO ✅
- Monitor your main domain and important endpoints
- Use HEAD requests for simple "keep-alive" pings
- Use GET with keyword checks for functionality tests
- Set up email alerts
- Check dashboard weekly
- Use 5-minute intervals (free tier) for main site

### DON'T ❌
- Don't monitor every single page (waste of monitors)
- Don't use 1-minute intervals on Vercel free tier (may hit limits)
- Don't monitor development/local environments
- Don't rely solely on UptimeRobot (use multiple tools)
- Don't ignore alerts (fix issues promptly)

---

## Alternative Monitoring Tools

### Free Alternatives

**1. Cronitor** (https://cronitor.io)
- Similar to UptimeRobot
- Cron job monitoring
- Free tier: 5 monitors

**2. Better Uptime** (https://betteruptime.com)
- Modern UI
- Incident management
- Free tier: 10 monitors

**3. Freshping** (https://www.freshworks.com/website-monitoring/)
- 50 free monitors
- 1-minute checks
- Global monitoring

**4. StatusCake** (https://www.statuscake.com/)
- Unlimited monitors (free)
- Page speed monitoring
- SSL monitoring

### Paid Options

**1. Pingdom** (https://www.pingdom.com/)
- Enterprise-grade
- Detailed reports
- From $10/month

**2. New Relic** (https://newrelic.com/)
- Full APM (Application Performance Monitoring)
- Real user monitoring
- From $99/month

**3. Datadog** (https://www.datadoghq.com/)
- Infrastructure monitoring
- Log management
- Custom metrics

---

## Vercel-Specific Considerations

### Vercel Free Tier Limits
- 100GB bandwidth/month
- 100 hours serverless function execution/month
- UptimeRobot uses minimal bandwidth (~10MB/month)

### Vercel Analytics
Vercel also provides built-in analytics:
1. Go to Vercel Dashboard → Your Project → Analytics
2. See:
   - Page views
   - Response times
   - Errors
   - Geographic distribution

**Use both UptimeRobot + Vercel Analytics for complete monitoring!**

---

## Troubleshooting

### Monitor Shows "Down" but Site Works

**Possible causes:**
- Timeout too short (increase to 30s)
- Temporary Vercel issue
- DNS propagation delay
- Firewall blocking UptimeRobot IPs

**Solution:**
1. Increase timeout to 30 seconds
2. Check Vercel status: https://www.vercel-status.com/
3. Verify URL is correct
4. Test manually: `curl -I https://your-app.vercel.app`

### High Response Times

**Normal for Vercel:**
- Cold start: 5-15 seconds (first request)
- Warm: 100-500ms

**If consistently slow (>3 seconds warm):**
- Check database query performance
- Review Vercel logs
- Consider upgrading to Vercel Pro
- Optimize Django queries

### Too Many False Alerts

**Solutions:**
- Increase monitoring interval (5 → 10 minutes)
- Increase timeout (30 → 60 seconds)
- Use "Alert me after X failed checks" (wait for 2-3 failures)
- Check if Vercel has scheduled maintenance

---

## Success Metrics

After setting up UptimeRobot, track:

📊 **Uptime:** Should be 99.5%+ 
⚡ **Response Time:** <2 seconds average  
🐛 **Incidents:** <5 per month  
❄️ **Cold Starts:** Eliminated (always warm)  

---

## Next Steps After Setup

1. ✅ Create UptimeRobot account
2. ✅ Add monitor for your Vercel deployment
3. ✅ Set up email alerts
4. ✅ Wait 24 hours and check statistics
5. ✅ Adjust intervals if needed
6. ✅ Add health check endpoint (optional)
7. ✅ Create public status page (optional)

---

## Quick Setup Checklist

- [ ] Created UptimeRobot account
- [ ] Added homepage monitor (5-minute interval)
- [ ] Added API health check (10-minute interval)
- [ ] Configured email alerts
- [ ] Tested monitor is working (shows "Up")
- [ ] Checked response times are reasonable
- [ ] Set up keyword monitoring (optional)
- [ ] Created public status page (optional)
- [ ] Noted uptime percentage baseline

---

## Support & Resources

- **UptimeRobot Docs:** https://uptimerobot.com/kb/
- **Vercel Status:** https://www.vercel-status.com/
- **Project Issues:** https://github.com/NotoriousArnav/EventHorizon/issues

**Your app will now stay warm 24/7! No more cold starts!** 🔥🚀

---

## Real User Experience Impact

### Before UptimeRobot
```
User 1 (first visit): ⏳ 12 seconds load time
User 2 (5 min later): ⏳ 11 seconds load time
User 3 (10 min later): ⚡ 200ms load time (caught warm)
User 4 (30 min later): ⏳ 13 seconds load time (cold again)
```

### After UptimeRobot
```
User 1: ⚡ 300ms load time
User 2: ⚡ 250ms load time
User 3: ⚡ 280ms load time
User 4: ⚡ 320ms load time
```

**Consistent, fast experience for everyone!**
