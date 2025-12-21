# Custom Domain Setup: events.neopanda.tech

Quick guide to configure your custom domain for Event Horizon on Vercel.

## Overview

Your setup:
- **Main domain**: neopanda.tech (Portfolio)
- **Subdomain**: events.neopanda.tech (Event Horizon)
- **Platform**: Vercel

---

## Step 1: Add Domain in Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your **Event Horizon** project
3. Go to **Settings** → **Domains**
4. Click **Add Domain**
5. Enter: `events.neopanda.tech`
6. Click **Add**

Vercel will show you DNS records to configure.

---

## Step 2: Configure DNS

### Option A: If you use Vercel DNS for neopanda.tech

Vercel will automatically configure the subdomain. Just wait 1-2 minutes!

### Option B: If you use external DNS (Cloudflare, Namecheap, etc.)

Add a **CNAME record** to your DNS provider:

```
Type:  CNAME
Name:  events
Target: cname.vercel-dns.com
TTL:   Auto (or 3600)
```

**Common DNS Providers:**

#### Cloudflare
1. Go to Cloudflare Dashboard → Your domain
2. Click **DNS** → **Records** → **Add record**
3. Type: `CNAME`
4. Name: `events`
5. Target: `cname.vercel-dns.com`
6. Proxy status: **Proxied** (orange cloud) ✅
7. Click **Save**

#### Namecheap
1. Advanced DNS → Add New Record
2. Type: `CNAME Record`
3. Host: `events`
4. Value: `cname.vercel-dns.com`
5. TTL: Automatic
6. Save

#### Google Domains
1. DNS → Custom records
2. Create new record
3. Type: `CNAME`
4. Host name: `events`
5. Data: `cname.vercel-dns.com`
6. Save

#### GoDaddy
1. DNS Management → Add record
2. Type: `CNAME`
3. Name: `events`
4. Value: `cname.vercel-dns.com`
5. TTL: 1 Hour
6. Save

---

## Step 3: Wait for DNS Propagation

- **Typical time**: 5-30 minutes
- **Maximum**: Up to 48 hours (rare)

Check propagation:
```bash
# Check if DNS is propagated
dig events.neopanda.tech

# Or use online tool
# https://dnschecker.org/#CNAME/events.neopanda.tech
```

---

## Step 4: Verify SSL Certificate

Vercel automatically provisions SSL certificates (Let's Encrypt):

1. In Vercel → Domains, check status
2. Should show: **Valid Configuration** ✅
3. SSL Certificate: **Active** 🔒

If there's an issue:
- Wait a few more minutes
- Check DNS is correct
- Remove and re-add domain

---

## Step 5: Update Environment Variables

Add to Vercel → Settings → Environment Variables:

```bash
ALLOWED_HOSTS=.vercel.app,events.neopanda.tech,neopanda.tech
```

**Note:** The `.vercel.app` is already auto-detected by the code, but adding `events.neopanda.tech` explicitly is good practice.

Redeploy after adding environment variables:
- Go to **Deployments**
- Click **...** on latest deployment
- Click **Redeploy**

---

## Step 6: Update OAuth Callback URLs

Once your domain is live, update OAuth providers:

### GitHub OAuth
1. Go to [GitHub OAuth Apps](https://github.com/settings/developers)
2. Select **Event Horizon** app
3. Update **Authorization callback URL**:
   ```
   https://events.neopanda.tech/accounts/github/login/callback/
   ```
4. Click **Update application**

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. APIs & Services → Credentials
3. Select your OAuth 2.0 Client ID
4. Add to **Authorized JavaScript origins**:
   ```
   https://events.neopanda.tech
   ```
5. Add to **Authorized redirect URIs**:
   ```
   https://events.neopanda.tech/accounts/google/login/callback/
   ```
6. Click **Save**

---

## Step 7: Update UptimeRobot

Update your monitors to use the custom domain:

1. Go to [UptimeRobot Dashboard](https://uptimerobot.com/dashboard)
2. Edit your monitor
3. Change URL from:
   - Old: `https://event-horizon-xxx.vercel.app`
   - New: `https://events.neopanda.tech`
4. Save

Or add as a new monitor to track both URLs.

---

## Step 8: Test Everything

### Basic Tests
```bash
# Check DNS resolution
dig events.neopanda.tech

# Check HTTPS works
curl -I https://events.neopanda.tech

# Check redirect (should work)
curl -I http://events.neopanda.tech
```

### Browser Tests
- [ ] Homepage loads: `https://events.neopanda.tech`
- [ ] HTTPS is enabled (lock icon) 🔒
- [ ] Static files load (CSS, images)
- [ ] Admin panel works: `https://events.neopanda.tech/admin/`
- [ ] GitHub OAuth works
- [ ] Google OAuth works
- [ ] Health check: `https://events.neopanda.tech/health/`

---

## Step 9: Set as Primary Domain (Optional)

In Vercel → Domains:
1. Find `events.neopanda.tech`
2. Click **...** → **Set as Primary**
3. All `.vercel.app` URLs will redirect to your custom domain

---

## Optional: Add Root Domain Redirect

If you want `neopanda.tech` to redirect to your portfolio but keep the subdomain:

### Already Have Portfolio at neopanda.tech?
✅ Perfect! Nothing to do. Just add the subdomain.

### Want Both?
You can have:
- `neopanda.tech` → Portfolio
- `events.neopanda.tech` → Event Horizon
- `blog.neopanda.tech` → Blog (future)
- `api.neopanda.tech` → API (future)

---

## Troubleshooting

### "Domain is not configured correctly"
- Check DNS record is correct: `CNAME events → cname.vercel-dns.com`
- Wait longer (DNS can take up to 48h, usually 5-30 min)
- Try removing and re-adding domain in Vercel

### "SSL certificate provisioning failed"
- Vercel needs domain to resolve to their servers first
- Check DNS propagation: `dig events.neopanda.tech`
- Should return Vercel's IP or CNAME
- Retry: Remove domain, wait 5 min, add again

### "DisallowedHost" Error
- Add domain to `ALLOWED_HOSTS` environment variable
- Redeploy after updating env vars
- Or wait for auto-detection (code checks `VERCEL_URL`)

### OAuth Doesn't Work on Custom Domain
- Update callback URLs in GitHub/Google
- Must be exact: `https://events.neopanda.tech/accounts/...`
- Include trailing slash: `/callback/`

### Static Files Not Loading
- Check Vercel logs
- Verify `collectstatic` ran during build
- Check WhiteNoise is enabled (already configured)

---

## DNS Record Reference

Your complete DNS setup should look like:

```
# Root domain (portfolio)
Type: A or CNAME
Name: @
Value: <your-portfolio-host>

# WWW redirect (optional)
Type: CNAME
Name: www
Value: neopanda.tech

# Event Horizon subdomain
Type: CNAME
Name: events
Value: cname.vercel-dns.com

# Other subdomains (future)
# Type: CNAME
# Name: blog
# Value: <blog-host>
```

---

## Security Considerations

### SSL/TLS
- ✅ Vercel automatically provisions SSL certificates
- ✅ HTTPS enforced (HTTP redirects to HTTPS)
- ✅ TLS 1.3 supported
- ✅ Auto-renewal (no manual work)

### HSTS (HTTP Strict Transport Security)
Already configured in Django settings:
```python
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Content Security Policy
Already configured via meta tags in base template.

---

## Monitoring

### Set Up Monitoring for Custom Domain

1. **UptimeRobot**: Monitor `events.neopanda.tech`
2. **Vercel Analytics**: Automatic for custom domains
3. **Google Search Console**: 
   - Add `events.neopanda.tech` as property
   - Submit sitemap: `https://events.neopanda.tech/sitemap.xml`

---

## Marketing & SEO

### Update Metadata

Once domain is live, verify these are correct:

- **Sitemap**: `https://events.neopanda.tech/sitemap.xml`
- **Robots.txt**: `https://events.neopanda.tech/robots.txt`
- **OG Image**: Should show Event Horizon logo
- **Structured Data**: Should be valid (test in Google Rich Results)

### Submit to Search Engines

```bash
# Google
https://search.google.com/search-console

# Bing
https://www.bing.com/webmasters

# Sitemap URL to submit
https://events.neopanda.tech/sitemap.xml
```

---

## Future Enhancements

### Email Domain
Setup email with custom domain:
```
noreply@neopanda.tech
support@neopanda.tech
events@neopanda.tech
```

Use services like:
- Gmail with custom domain (Google Workspace)
- SendGrid
- Mailgun
- AWS SES

### CDN for Media
If you have lots of images/media:
- Use Cloudflare CDN
- Already get Vercel's Edge Network
- Or use Cloudinary for image optimization

---

## Quick Reference

**Your URLs:**
```
Production:     https://events.neopanda.tech
Vercel Default: https://event-horizon-xxx.vercel.app (redirects)
Admin Panel:    https://events.neopanda.tech/admin/
Health Check:   https://events.neopanda.tech/health/
API:            https://events.neopanda.tech/api/v1/
Sitemap:        https://events.neopanda.tech/sitemap.xml
```

**DNS Record:**
```
Type:   CNAME
Name:   events
Target: cname.vercel-dns.com
```

**OAuth Callbacks:**
```
GitHub: https://events.neopanda.tech/accounts/github/login/callback/
Google: https://events.neopanda.tech/accounts/google/login/callback/
```

---

## Next Steps

1. ✅ Add domain in Vercel
2. ✅ Configure DNS CNAME record
3. ✅ Wait for propagation (5-30 min)
4. ✅ Verify SSL certificate is active
5. ✅ Update `ALLOWED_HOSTS` environment variable
6. ✅ Redeploy
7. ✅ Update OAuth callback URLs
8. ✅ Update UptimeRobot monitors
9. ✅ Test everything
10. ✅ Submit sitemap to search engines

**Your Event Horizon will be live at events.neopanda.tech! 🚀**

---

## Support

- **Vercel Docs**: https://vercel.com/docs/custom-domains
- **DNS Checker**: https://dnschecker.org/
- **SSL Test**: https://www.ssllabs.com/ssltest/
- **Project Issues**: https://github.com/NotoriousArnav/EventHorizon/issues

**10x fun with your custom domain!** 🎉
