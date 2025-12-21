# Supabase Storage Setup Guide

This guide explains how to configure EventHorizon to use Supabase Storage as your S3-compatible storage backend.

## Overview

Supabase Storage provides S3-compatible object storage that integrates seamlessly with your Supabase project. It offers:

- **Integrated with Supabase**: Same dashboard as your database
- **Row Level Security**: Fine-grained access control (optional)
- **Global CDN**: Fast file delivery worldwide
- **Generous Free Tier**: Perfect for getting started
- **Image Transformations**: On-the-fly image resizing and optimization

## Prerequisites

- A Supabase project (already set up for your database)
- Storage bucket created in Supabase
- S3 Access Keys generated

## Step 1: Create a Storage Bucket

1. Go to your Supabase Dashboard
2. Navigate to **Storage** in the left sidebar
3. Click **New bucket**
4. Configure your bucket:
   - **Name**: `eventhorizon` (or your preferred name)
   - **Public bucket**: ✅ Check this (for public avatars and images)
   - **File size limit**: Set to 5MB (matches our compression limit)
   - **Allowed MIME types**: Leave empty for all types, or set to `image/*` for images only

## Step 2: Generate S3 Access Keys

1. In your Supabase Dashboard, go to **Settings** > **API**
2. Scroll down to **S3 Access Keys** section
3. Click **Generate new key**
4. Save these credentials securely:
   - **Access Key ID**: Starts with `sb...`
   - **Secret Access Key**: Long random string
   - **Endpoint**: Your project's S3 endpoint URL

## Step 3: Configure EventHorizon

Edit your `.env` file and add/update the following configuration:

```bash
# ===========================
# Supabase S3 Storage Configuration
# ===========================
STORAGE_BACKEND=s3

# S3 Credentials from Supabase Dashboard > Settings > API > S3 Access Keys
AWS_ACCESS_KEY_ID=sbxxxxxxxxxxxxxxxxxx
AWS_SECRET_ACCESS_KEY=your-secret-key-here
AWS_STORAGE_BUCKET_NAME=eventhorizon  # Your bucket name from Step 1

# Supabase S3 Endpoint (from your dashboard)
# Format: https://<project-ref>.supabase.co/storage/v1/s3
AWS_S3_ENDPOINT_URL=https://your-project-ref.supabase.co/storage/v1/s3

# Standard configuration
AWS_S3_REGION_NAME=us-east-1
AWS_S3_USE_SSL=True

# Optional: Custom domain for faster access via CDN
# Format: <project-ref>.supabase.co/storage/v1/object/public/<bucket-name>
AWS_S3_CUSTOM_DOMAIN=your-project-ref.supabase.co/storage/v1/object/public/eventhorizon
```

## Step 4: Find Your Project Reference

Your project reference is in your Supabase project URL:

```
https://abcdefghijklmnop.supabase.co
        ^^^^^^^^^^^^^^^^
        This is your project-ref
```

Use it to construct your URLs:
- **S3 Endpoint**: `https://abcdefghijklmnop.supabase.co/storage/v1/s3`
- **CDN Domain**: `abcdefghijklmnop.supabase.co/storage/v1/object/public/eventhorizon`

## Step 5: Set Bucket Permissions

For public access to uploaded files (avatars, event images):

1. Go to **Storage** > Your bucket (`eventhorizon`)
2. Click **Policies** tab
3. Add a new policy:

```sql
-- Allow public read access to all files
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'eventhorizon' );

-- Allow authenticated uploads (optional - Django handles auth)
CREATE POLICY "Authenticated Uploads"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'eventhorizon' );
```

Alternatively, for a simpler setup, just ensure your bucket is marked as **Public** in Step 1.

## Step 6: Test the Configuration

1. Restart your Django development server:
   ```bash
   uv run python manage.py runserver
   ```

2. Log in and go to your profile
3. Upload an avatar image
4. Verify the image uploads successfully and displays correctly

## Image Compression

EventHorizon automatically compresses all uploaded profile pictures to ensure they're under 5MB. The compression happens before upload to save bandwidth and storage costs.

**Compression Details:**
- **Max file size**: 5MB
- **Max dimensions**: 2048x2048 pixels
- **Format**: JPEG (converted from PNG/WEBP if needed)
- **Quality**: 85% (adjusts down if needed to meet size limit)

You can see compression logs in your console:
```
INFO Avatar compressed for user arnav: 8.24 MB -> 2.87 MB (65.2% reduction)
```

## Troubleshooting

### Files not uploading

**Check credentials:**
```bash
# Verify your .env settings are loaded
uv run python manage.py shell
>>> from django.conf import settings
>>> print(settings.AWS_ACCESS_KEY_ID)
>>> print(settings.AWS_S3_ENDPOINT_URL)
```

**Check bucket exists:**
- Go to Supabase Dashboard > Storage
- Verify bucket name matches `AWS_STORAGE_BUCKET_NAME`

### "Access Denied" errors

**Check bucket is public:**
1. Go to Storage > Your bucket
2. Click the settings icon
3. Ensure "Public bucket" is enabled

**Check policies:**
- Go to Policies tab
- Ensure SELECT policy exists for public access

### Images not loading

**Check Custom Domain:**
- If using `AWS_S3_CUSTOM_DOMAIN`, ensure it's correctly formatted
- Remove `https://` prefix - Django adds it automatically
- Include the full path: `<project-ref>.supabase.co/storage/v1/object/public/<bucket-name>`

**Test URLs directly:**
- Get a file URL from Django: `user.profile.avatar.url`
- Open it in a browser
- If it 404s, check bucket policies and public access settings

### SSL Certificate errors

**Ensure SSL is enabled:**
```bash
AWS_S3_USE_SSL=True
```

**Check endpoint URL format:**
- Must start with `https://` (not `http://`)
- Must be your project's actual Supabase URL

## Cost Optimization

Supabase Storage pricing (as of 2024):

| Tier | Storage | Bandwidth | Price |
|------|---------|-----------|-------|
| Free | 1 GB | 2 GB | $0 |
| Pro | 100 GB | 200 GB | $25/mo |

**Tips to reduce costs:**
1. **Image Compression**: Already handled by EventHorizon (max 5MB)
2. **CDN Caching**: Use `AWS_S3_CUSTOM_DOMAIN` for better caching
3. **Cleanup Old Files**: Periodically remove unused avatars
4. **Lifecycle Policies**: Auto-delete old versions (if versioning enabled)

## Migration from MinIO/Local Storage

If you're migrating from MinIO or local filesystem storage:

### Option 1: Manual Upload (for small datasets)

```bash
# Install AWS CLI
pip install awscli

# Configure AWS CLI with Supabase credentials
aws configure --profile supabase
# Enter your AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, region (us-east-1)

# Sync files
aws s3 sync media/ s3://eventhorizon/media/ \
  --endpoint-url=https://your-project-ref.supabase.co/storage/v1/s3 \
  --profile supabase
```

### Option 2: Using Django Management Command

```bash
# Use the provided migration script
uv run python migrate_media_to_s3.py
```

This script will:
- Connect to both old and new storage
- Copy files with progress tracking
- Verify file integrity
- Update database references

## Advanced Configuration

### Image Transformations

Supabase Storage supports on-the-fly image transformations:

```python
# In your templates
{{ user.profile.avatar.url }}?width=200&height=200
```

Supported parameters:
- `width`: Resize width
- `height`: Resize height
- `quality`: JPEG quality (1-100)
- `format`: Output format (webp, avif, etc.)

### Private Files

For files that shouldn't be publicly accessible:

```python
# In models.py
from storage.s3 import S3PrivateStorage

class Document(models.Model):
    file = models.FileField(storage=S3PrivateStorage())
```

Create a private bucket in Supabase and disable public access.

### Custom Upload Paths

```python
# In models.py
def user_avatar_path(instance, filename):
    return f'avatars/{instance.user.id}/{filename}'

class Profile(models.Model):
    avatar = models.ImageField(upload_to=user_avatar_path, ...)
```

## Security Best Practices

1. **Rotate Keys Regularly**: Generate new S3 access keys every 90 days
2. **Use Environment Variables**: Never commit credentials to git
3. **Enable Versioning**: Protect against accidental deletions
4. **Set File Size Limits**: Already configured (5MB max)
5. **Validate File Types**: Django handles this via `ImageField`
6. **Use HTTPS**: Already configured (`AWS_S3_USE_SSL=True`)

## Support

For Supabase-specific issues:
- [Supabase Storage Docs](https://supabase.com/docs/guides/storage)
- [Supabase Discord](https://discord.supabase.com/)

For EventHorizon integration issues:
- Check [Storage Overview](./overview.md)
- Review [Technical Quirks](../technical_quirks.md)
- Open a GitHub issue

## Next Steps

- ✅ Configure backup strategy
- ✅ Set up monitoring and alerts
- ✅ Enable image transformations (optional)
- ✅ Configure CDN caching headers
- ✅ Plan media file cleanup strategy
