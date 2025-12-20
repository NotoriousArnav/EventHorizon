# EventHorizon Production Deployment Guide

## Email Configuration Options

EventHorizon supports multiple email backends for production. Choose based on your needs:

### Option 1: SMTP (Gmail, AWS SES, Custom Server)

**Best for:** Small to medium deployments, existing email infrastructure

```bash
# .env configuration
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Gmail Setup:**
1. Enable 2FA on your Google account
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character password as `EMAIL_HOST_PASSWORD`

**AWS SES Setup:**
```bash
EMAIL_HOST=email-smtp.us-east-1.amazonaws.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-ses-smtp-username
EMAIL_HOST_PASSWORD=your-ses-smtp-password
```

### Option 2: SendGrid

**Best for:** High-volume transactional emails, detailed analytics

```bash
# Install package
uv add sendgrid-django

# .env configuration
EMAIL_BACKEND=sendgrid
SENDGRID_API_KEY=SG.your-api-key-here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### Option 3: Mailgun

**Best for:** Developer-friendly API, EU hosting options

```bash
# Install package
uv add django-anymail

# .env configuration
EMAIL_BACKEND=mailgun
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_SENDER_DOMAIN=mg.yourdomain.com
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

## Testing Email Configuration

```bash
# Send test email
python manage.py shell

>>> from django.core.mail import send_mail
>>> send_mail(
...     'Test Subject',
...     'Test message from EventHorizon',
...     'noreply@yourdomain.com',
...     ['recipient@example.com'],
... )
```

Or use Django's built-in test command (Django 3.0+):
```bash
python manage.py sendtestemail your-email@example.com
```

## Email Usage in EventHorizon

Emails are sent for:
- **Registration status changes** (`events/views.py:385`, `events/views.py:401`, `events/views.py:418`)
  - Approval notifications
  - Waitlist notifications
  - Cancellation notifications
- **Password reset** (django-allauth)
- **Email verification** (django-allauth)

## Common Email Issues

### Gmail "Less secure app access" error
**Solution:** Use App Passwords (requires 2FA)

### Emails going to spam
**Solutions:**
- Set up SPF, DKIM, and DMARC records for your domain
- Use a reputable email service (SendGrid, Mailgun, AWS SES)
- Use a verified sender domain
- Include unsubscribe links

### Rate limiting
**Solutions:**
- Gmail: 500 emails/day limit
- SendGrid Free: 100 emails/day
- Mailgun Free: 5,000 emails/month
- AWS SES: Request production access (starts in sandbox)

## Production Checklist

- [ ] Set `EMAIL_BACKEND` to smtp/sendgrid/mailgun
- [ ] Configure email credentials securely
- [ ] Set `DEFAULT_FROM_EMAIL` to your domain
- [ ] Test email sending with test command
- [ ] Configure DNS records (SPF, DKIM, DMARC)
- [ ] Monitor email delivery rates
- [ ] Set up email failure logging

## Security Best Practices

1. **Never commit credentials** - Use environment variables
2. **Use App Passwords** - Don't use your main account password
3. **Enable TLS** - Always use `EMAIL_USE_TLS=True` for SMTP
4. **Rotate credentials** - Change API keys periodically
5. **Monitor usage** - Watch for suspicious sending patterns

## Example Production .env

```bash
# Production Email (Gmail)
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@eventhorizon.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop  # App password
DEFAULT_FROM_EMAIL=Event Horizon <noreply@eventhorizon.com>
SERVER_EMAIL=alerts@eventhorizon.com
```

## Monitoring

Track email health with:
- SendGrid: Built-in analytics dashboard
- Mailgun: Events API and webhooks
- AWS SES: CloudWatch metrics
- SMTP: Server logs and bounce handling

For production, consider setting up bounce and complaint handling to maintain sender reputation.
