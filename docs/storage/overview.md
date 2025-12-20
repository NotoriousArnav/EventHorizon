# Storage System Overview

EventHorizon uses a flexible, provider-agnostic storage system that allows you to easily switch between different storage backends with minimal configuration changes.

## Architecture

The storage system is designed with the following principles:

1. **Provider Agnostic**: Single interface for all storage operations
2. **Django Integration**: Leverages Django's storage backend system
3. **Easy Configuration**: Switch providers via environment variables
4. **Fallback Support**: Graceful degradation to local storage for development
5. **Community Friendly**: Well-documented with examples for each provider

## Supported Storage Backends

### Currently Supported

- **Local Filesystem** (default) - For development
- **S3-Compatible Storage**:
  - AWS S3
  - MinIO (recommended for local development)
  - DigitalOcean Spaces
  - Cloudflare R2
  - Backblaze B2
  - Any S3-compatible storage service

### Coming Soon

- **Supabase Storage** - PostgreSQL-backed storage
- **Vercel Blob** - Edge-optimized storage
- **Google Cloud Storage** - GCS buckets
- **Azure Blob Storage** - Microsoft Azure storage

## How It Works

```
┌─────────────────────────────────────────────────┐
│         Django Models (ImageField, etc.)        │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│      Storage Backend (configured in settings)   │
│  - Provider selection based on env vars         │
└──────────────────┬──────────────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
┌─────▼─────┐ ┌───▼───┐ ┌─────▼──────┐
│ Local FS  │ │  S3   │ │  Supabase  │
│           │ │ MinIO │ │   (soon)   │
└───────────┘ └───────┘ └────────────┘
```

## Quick Start

### 1. Choose Your Storage Backend

Set the `STORAGE_BACKEND` environment variable in your `.env` file:

```bash
# Local filesystem (default)
STORAGE_BACKEND=local

# S3-compatible storage
STORAGE_BACKEND=s3

# MinIO (alias for s3)
STORAGE_BACKEND=minio
```

### 2. Configure Provider Credentials

Add the required credentials for your chosen provider. See provider-specific guides:

- [MinIO Setup](./minio.md) - Local development
- [AWS S3 Setup](./aws-s3.md) - Production
- [Other S3-Compatible Providers](./s3-compatible.md) - DigitalOcean, Cloudflare R2, etc.

### 3. Test Your Configuration

```bash
# Run migrations (if any)
python manage.py migrate

# Test file upload by updating your profile picture
# through the web interface or Django admin
```

## File Organization

Files are organized in the following structure:

```
bucket/
├── media/              # User-uploaded files
│   ├── avatars/        # User profile pictures
│   │   └── users/
│   │       └── {user_id}/
│   │           └── {unique_id}.jpg
│   └── events/         # Event-related uploads (future)
├── static/             # Static files (CSS, JS, images)
│   └── ...
└── private/            # Private files (optional)
    └── ...
```

## Storage Classes

EventHorizon provides three storage classes:

### 1. Media Storage (Public)

Used for user-uploaded content that should be publicly accessible:

```python
from storage.s3 import S3MediaStorage

class Profile(models.Model):
    avatar = models.ImageField(storage=S3MediaStorage())
```

**Features:**
- Public read access
- Files stored with unique names to prevent overwrites
- Automatic URL generation
- CDN support

### 2. Static Storage (Public)

Used for static files (CSS, JS, images):

```python
# In settings.py
STATICFILES_STORAGE = "storage.s3.S3StaticStorage"
```

**Features:**
- Public read access
- File overwriting enabled (for `collectstatic`)
- Long cache times
- CDN support

### 3. Private Storage

Used for files that should only be accessible to authorized users:

```python
from storage.s3 import S3PrivateStorage

class Invoice(models.Model):
    file = models.FileField(storage=S3PrivateStorage())
```

**Features:**
- Private access only
- Pre-signed URLs with expiration (default: 1 hour)
- No CDN caching

## Environment Variables

All storage configuration is done via environment variables in `.env`:

```bash
# Storage Backend Selection
STORAGE_BACKEND=s3  # Options: local, s3, minio

# S3 Configuration (when STORAGE_BACKEND=s3 or minio)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_ENDPOINT_URL=http://localhost:9000  # Optional: for MinIO/custom endpoints
AWS_S3_USE_SSL=True  # Set to False for local MinIO
AWS_S3_CUSTOM_DOMAIN=cdn.example.com  # Optional: CDN domain
```

See `.env.example` for all available options.

## Migration Guide

### Migrating from Local to S3

1. **Backup your media files**:
   ```bash
   tar -czf media_backup.tar.gz media/
   ```

2. **Configure S3 in `.env`**:
   ```bash
   STORAGE_BACKEND=s3
   AWS_ACCESS_KEY_ID=...
   # ... other settings
   ```

3. **Upload existing files to S3**:
   ```bash
   # Using AWS CLI
   aws s3 sync media/ s3://your-bucket/media/
   
   # Or using a custom management command (coming soon)
   python manage.py migrate_media_to_s3
   ```

4. **Test the migration**:
   - Visit user profiles to ensure avatars load correctly
   - Upload a new file to verify write access

5. **Clean up local files** (optional):
   ```bash
   rm -rf media/  # Only after verifying everything works!
   ```

### Switching Between S3 Providers

Simply update your environment variables. The storage system is compatible with any S3-compatible service:

```bash
# From AWS S3
AWS_S3_ENDPOINT_URL=

# To MinIO
AWS_S3_ENDPOINT_URL=http://localhost:9000

# To DigitalOcean Spaces
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
```

## Troubleshooting

### Files not uploading

1. Check credentials in `.env`
2. Verify bucket exists and has correct permissions
3. Check bucket CORS settings (for web uploads)
4. Verify network connectivity to storage endpoint

### URLs not working

1. Check `AWS_S3_CUSTOM_DOMAIN` setting
2. Verify bucket has public read permissions
3. Check CDN configuration (if using)

### "Access Denied" errors

1. Verify IAM permissions for S3 user
2. Check bucket policy
3. Verify CORS configuration

## Performance Optimization

### CDN Integration

Use a CDN to serve files faster:

```bash
AWS_S3_CUSTOM_DOMAIN=cdn.example.com
```

### Caching

Configure appropriate cache headers:

```python
# In settings.py
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # 1 day
}
```

### Thumbnails

Consider using image processing services:
- AWS Lambda + S3 triggers
- Cloudinary
- imgix

## Security Best Practices

1. **Never commit credentials** - Use environment variables
2. **Use IAM roles** - In AWS, prefer IAM roles over access keys
3. **Restrict permissions** - Only grant necessary S3 permissions
4. **Enable versioning** - Protect against accidental deletions
5. **Use HTTPS** - Always use SSL in production
6. **Rotate keys** - Regularly rotate access keys

## Next Steps

- [MinIO Setup Guide](./minio.md) - Set up local development storage
- [AWS S3 Setup Guide](./aws-s3.md) - Configure production storage
- [S3-Compatible Providers](./s3-compatible.md) - Use alternative providers

## Support

For issues or questions:
- Check the [Technical Quirks](../technical_quirks.md) documentation
- Review provider-specific guides
- Open an issue on GitHub
