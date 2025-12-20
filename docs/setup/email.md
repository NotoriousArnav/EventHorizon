# Email Configuration Guide

EventHorizon sends transactional emails for registration notifications, password resets, and account verification. This guide covers production email setup.

## Quick Start

### Development (Default)
No configuration needed - emails print to console:

```bash
# .env
EMAIL_BACKEND=console  # or omit entirely
```

### Production with Gmail

```bash
# .env
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx-xxxx-xxxx-xxxx  # App password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Gmail App Password Setup:**
1. Enable 2FA: https://myaccount.google.com/security
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Select "Mail" and your device
4. Copy the 16-character password

## Supported Email Backends

### 1. SMTP (Universal)

Works with Gmail, AWS SES, Mailgun SMTP, custom servers.

```bash
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587                    # 587 for TLS, 465 for SSL
EMAIL_USE_TLS=True               # Use TLS (recommended)
EMAIL_USE_SSL=False              # Use SSL (alternative to TLS)
EMAIL_HOST_USER=your-username
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
SERVER_EMAIL=admin@yourdomain.com  # For error emails
```

**Common SMTP Hosts:**
- Gmail: `smtp.gmail.com:587`
- AWS SES: `email-smtp.us-east-1.amazonaws.com:587`
- Mailgun: `smtp.mailgun.org:587`
- SendGrid: `smtp.sendgrid.net:587`

### 2. SendGrid API

High-volume transactional email with analytics.

```bash
# Install
uv add sendgrid-django

# .env
EMAIL_BACKEND=sendgrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### 3. Mailgun API

Developer-friendly with EU hosting options.

```bash
# Install
uv add django-anymail

# .env
EMAIL_BACKEND=mailgun
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_SENDER_DOMAIN=mg.yourdomain.com
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Testing Email Configuration

### Method 1: Django Shell

```bash
uv run python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    subject='Test Email from EventHorizon',
    message='If you receive this, email is configured correctly!',
    from_email='noreply@yourdomain.com',
    recipient_list=['your-email@example.com'],
    fail_silently=False,
)
```

### Method 2: Test Registration Email

1. Create an event as an organizer
2. Register for the event as a participant
3. As organizer, approve/waitlist/cancel the registration
4. Check the participant's email

## Email Types Sent by EventHorizon

| Email Type | Trigger | Template Location |
|------------|---------|-------------------|
| Registration Approved | Organizer approves waitlisted participant | `events/views.py:385` |
| Registration Waitlisted | Organizer moves participant to waitlist | `events/views.py:401` |
| Registration Cancelled | Organizer cancels registration | `events/views.py:418` |
| Password Reset | User requests password reset | django-allauth |
| Email Verification | User signs up | django-allauth |

## Troubleshooting

### Emails not sending

1. **Check email backend:**
   ```python
   from django.conf import settings
   print(settings.EMAIL_BACKEND)
   ```

2. **Test with fail_silently=False:**
   ```python
   send_mail(..., fail_silently=False)  # Shows errors
   ```

3. **Check credentials:**
   - Verify `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD`
   - For Gmail, ensure you're using an App Password, not your account password

### Emails going to spam

**Solutions:**
- **SPF Record:** Add to DNS: `v=spf1 include:_spf.google.com ~all` (for Gmail)
- **DKIM:** Configure in your email provider's settings
- **DMARC:** Add DNS record: `v=DMARC1; p=none; rua=mailto:postmaster@yourdomain.com`
- **Verified Domain:** Use a domain you own for `DEFAULT_FROM_EMAIL`
- **Consistent From Address:** Always use the same sender

### Rate Limits

| Provider | Free Tier Limit |
|----------|----------------|
| Gmail | 500 emails/day |
| SendGrid | 100 emails/day |
| Mailgun | 5,000 emails/month |
| AWS SES | 62,000/month (after leaving sandbox) |

**Solutions:**
- Upgrade to paid tier
- Implement email queuing (celery + django-celery-email)
- Batch notifications

### Gmail "Less secure app" error

**Solution:** Enable 2FA and use App Passwords (see Quick Start above)

### AWS SES Sandbox

New AWS SES accounts start in sandbox mode:
- Can only send to verified email addresses
- Limited to 200 emails/day

**To leave sandbox:**
1. Go to AWS SES Console
2. Request production access
3. Provide use case details
4. Wait for approval (usually 24 hours)

## Production Best Practices

### 1. Security
- ✅ Use environment variables for credentials
- ✅ Never commit `.env` to git
- ✅ Use TLS/SSL for SMTP
- ✅ Rotate API keys periodically
- ✅ Use App Passwords, not account passwords

### 2. Deliverability
- ✅ Configure SPF, DKIM, DMARC
- ✅ Use a verified sender domain
- ✅ Monitor bounce rates
- ✅ Implement unsubscribe handling
- ✅ Maintain clean recipient lists

### 3. Monitoring
- ✅ Set up email failure logging
- ✅ Track delivery rates
- ✅ Monitor for unusual sending patterns
- ✅ Set up bounce and complaint webhooks

### 4. Scalability
- ✅ Use dedicated email service (SendGrid, Mailgun, SES)
- ✅ Implement email queuing for high volume
- ✅ Set up retry logic for failures
- ✅ Consider async task processing (Celery)

## Example Production Configurations

### Small Deployment (< 1000 emails/month)
```bash
# Gmail SMTP - Simple and free
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Event Horizon <noreply@yourdomain.com>
```

### Medium Deployment (1K-10K emails/month)
```bash
# SendGrid API - Analytics and reliability
EMAIL_BACKEND=sendgrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Large Deployment (> 10K emails/month)
```bash
# AWS SES - Cost-effective at scale
EMAIL_BACKEND=smtp
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Advanced: Custom Email Templates

EventHorizon uses inline text for notification emails. To customize:

1. **Edit email content:** `events/views.py:385-424`
2. **Create HTML templates:** Extend to use `send_mail` with `html_message` parameter
3. **Use template engine:** Consider django-templated-email for complex layouts

Example with HTML:
```python
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

subject = f"Mission Status Update: APPROVED - {event.title}"
text_content = "Your application has been approved."
html_content = render_to_string('emails/approval.html', {'event': event})

msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
msg.attach_alternative(html_content, "text/html")
msg.send()
```

## Need Help?

- **Django Email Docs:** https://docs.djangoproject.com/en/stable/topics/email/
- **SendGrid Docs:** https://docs.sendgrid.com/for-developers/sending-email/django
- **Mailgun Docs:** https://documentation.mailgun.com/en/latest/
- **AWS SES Docs:** https://docs.aws.amazon.com/ses/
