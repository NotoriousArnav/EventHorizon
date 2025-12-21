# Email Verification Setup

Event Horizon includes mandatory email verification for new user registrations using Django Allauth.

## Features

- **Mandatory Email Verification**: All new users must verify their email address before they can log in
- **Beautiful Email Templates**: Futuristic-themed HTML and plain text emails
- **Auto-login After Verification**: Users are automatically logged in after clicking the verification link
- **3-Day Expiration**: Verification links expire after 3 days for security
- **Re-send Verification**: Users can request a new verification email from the email management page

## How It Works

### 1. User Registration

When a user signs up:
1. They enter username, email, and password
2. Account is created but not activated
3. Verification email is sent to their email address
4. User sees a "Verification Sent" page

### 2. Email Verification

The user receives an email with:
- Beautiful HTML design (Event Horizon themed)
- Plain text fallback for email clients that don't support HTML
- Verification button and plain URL
- 3-day expiration notice

### 3. Activation

When user clicks the verification link:
- Email address is marked as verified
- User is automatically logged in
- Redirected to their profile page

## Configuration

Settings are configured in `EventHorizon/settings.py`:

```python
# Email Verification Settings
ACCOUNT_EMAIL_REQUIRED = True  # Email is required for signup
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Options: "none", "optional", "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # Allow login with username or email
ACCOUNT_USERNAME_REQUIRED = True  # Username is required
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3  # Verification link expires after 3 days
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True  # Auto-login after email verification

# Social Account Settings (GitHub, Google)
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"  # Don't require verification for social logins
SOCIALACCOUNT_AUTO_SIGNUP = True  # Auto-create account from social login
SOCIALACCOUNT_QUERY_EMAIL = True  # Request email from social providers
```

## Email Templates

Three templates control the verification email:

### 1. Subject Line
`templates/account/email/email_confirmation_subject.txt`
```
Confirm Your Email Address - Event Horizon
```

### 2. Plain Text Email
`templates/account/email/email_confirmation_message.txt`

Used as fallback for email clients that don't support HTML.

### 3. HTML Email
`templates/account/email/email_confirmation_message.html`

Beautiful, futuristic-themed HTML email with:
- Event Horizon branding
- Gradient backgrounds
- Large "Verify Email Address" button
- Responsive design

## Testing Email Verification

### Development (Console Backend)

By default, emails are printed to the console:

```bash
uv run python manage.py runserver
```

When a user registers, you'll see the email in your terminal:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Confirm Your Email Address - Event Horizon
From: noreply@eventhorizon.local
To: user@example.com
Date: Sat, 21 Dec 2024 19:00:00 -0000
Message-ID: <...>

Welcome to Event Horizon!

You're receiving this transmission because you initiated registration at 127.0.0.1:8000.

To complete your registration and activate your account, please verify your email address by clicking the link below:

http://127.0.0.1:8000/accounts/confirm-email/MQ:1tK7Zx:...

This verification link will expire in 3 days.
```

Copy the verification URL and paste it in your browser to test.

### Production (SMTP)

Configure SMTP in `.env`:

```bash
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

## User Experience Flow

### 1. Registration Page
`/accounts/signup/`

User fills out:
- Username
- Email
- Password (twice)

### 2. Verification Sent Page
`/accounts/verification-sent/`

Shows message: "We have dispatched a verification signal to your email address."

### 3. Email Inbox

User receives beautifully formatted email with verification link.

### 4. Email Confirmation
`/accounts/confirm-email/<key>/`

When user clicks the link:
- Email is verified
- User is logged in automatically
- Redirected to profile page

### 5. Email Management
`/accounts/email/`

Users can:
- View all email addresses
- See verification status (verified/unverified badges)
- Set primary email
- Add new email addresses
- Re-send verification emails
- Remove email addresses

## Managing Email Addresses

Users can manage their email addresses at `/accounts/email/`:

**Features:**
- View all associated email addresses
- See verification status (green badge = verified, yellow = unverified)
- See primary email (blue badge)
- Re-send verification emails
- Add additional email addresses
- Remove old email addresses
- Set different primary email

## Social Login Exception

Users who register via GitHub or Google OAuth:
- **Do NOT** need to verify their email
- Email is automatically marked as verified (trusted from provider)
- Can log in immediately after OAuth authorization

This is configured via:
```python
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
```

## Customization

### Change Verification Expiration

In `settings.py`:
```python
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7  # Change to 7 days
```

### Disable Auto-Login After Verification

```python
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
```

### Make Email Verification Optional

```python
ACCOUNT_EMAIL_VERIFICATION = "optional"  # User can login before verifying
```

### Allow Login Without Username

```python
ACCOUNT_AUTHENTICATION_METHOD = "email"  # Only email, no username
ACCOUNT_USERNAME_REQUIRED = False
```

## Troubleshooting

### Email Not Sending

**Check email backend:**
```bash
uv run python manage.py shell
>>> from django.conf import settings
>>> print(settings.EMAIL_BACKEND)
django.core.mail.backends.console.EmailBackend  # Development
```

**Test email sending:**
```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'This is a test.',
    'noreply@eventhorizon.local',
    ['test@example.com'],
    fail_silently=False,
)
```

### Verification Link Not Working

**Check Site configuration:**
1. Go to Django admin: `/admin/sites/site/`
2. Make sure Domain matches your current domain
   - Development: `127.0.0.1:8000`
   - Production: `yourdomain.com`

### User Can't Login

**Check if email is verified:**
```bash
uv run python manage.py shell
>>> from users.models import User
>>> user = User.objects.get(username='testuser')
>>> user.emailaddress_set.all()
<QuerySet [<EmailAddress: testuser@example.com (unverified)>]>
```

If unverified, re-send verification email via `/accounts/email/`.

### Gmail Blocking Emails

If using Gmail SMTP and emails aren't sending:

1. **Use App Password**: Regular passwords don't work
   - Go to: https://myaccount.google.com/apppasswords
   - Generate app-specific password
   - Use that in `EMAIL_HOST_PASSWORD`

2. **Check Less Secure Apps**: Make sure 2FA is enabled (required for App Passwords)

3. **Check Sent Mail**: Login to Gmail and check Sent folder

## Security Considerations

1. **HTTPS Required**: In production, always use HTTPS to protect verification links
2. **Short Expiration**: 3-day expiration prevents old links from being exploited
3. **One-Time Use**: Verification links can only be used once
4. **Rate Limiting**: Consider adding rate limiting to prevent abuse
5. **Email Ownership**: Only the email owner can verify (link sent to their inbox)

## Next Steps

- Configure production SMTP settings in `.env`
- Test the full registration flow
- Customize email templates with your branding
- Set up email delivery monitoring (e.g., SendGrid, Mailgun)
- Consider adding email verification reminders

## Related Documentation

- [Email Configuration](../setup/email.md) - Setting up SMTP providers
- [Authentication](../features/users.md) - User authentication features
- [OAuth Setup](../features/oauth.md) - GitHub/Google login setup
