# EventHorizon Storage Module

Flexible, provider-agnostic storage system for EventHorizon that supports multiple storage backends including local filesystem, S3-compatible storage (AWS S3, MinIO, DigitalOcean Spaces, Cloudflare R2), and more.

## Quick Start

### Local Development (Default)

No configuration needed! By default, EventHorizon uses local filesystem storage:

```bash
# In your .env (or leave STORAGE_BACKEND unset)
STORAGE_BACKEND=local
```

Files are stored in `media/` directory.

### MinIO (Recommended for Development)

MinIO provides S3-compatible storage that runs locally:

```bash
# 1. Start MinIO with Docker
docker run -d \
  --name minio \
  -p 9000:9000 -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  quay.io/minio/minio server /data --console-address ":9001"

# 2. Configure EventHorizon (.env)
STORAGE_BACKEND=minio
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_STORAGE_BUCKET_NAME=eventhorizon
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_S3_USE_SSL=False
AWS_S3_REGION_NAME=us-east-1

# 3. Create bucket and set permissions
# Visit http://localhost:9001 and create 'eventhorizon' bucket
```

See [docs/storage/minio.md](../docs/storage/minio.md) for detailed setup.

### AWS S3 (Production)

```bash
# In your .env
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_USE_SSL=True
```

## Features

- **Provider Agnostic**: Switch between providers with a single environment variable
- **S3-Compatible**: Works with AWS S3, MinIO, DigitalOcean Spaces, Cloudflare R2, Backblaze B2
- **Django Integration**: Seamless integration with Django's file storage system
- **Multiple Storage Classes**: Public media, private files, static files
- **CDN Support**: Optional CDN integration for faster file serving
- **Easy Migration**: Migrate between providers without code changes

## Supported Backends

| Backend | Status | Use Case |
|---------|--------|----------|
| Local Filesystem | ✅ Ready | Development |
| AWS S3 | ✅ Ready | Production |
| MinIO | ✅ Ready | Local development, Self-hosted |
| DigitalOcean Spaces | ✅ Ready | Production (cost-effective) |
| Cloudflare R2 | ✅ Ready | Production (no egress fees) |
| Supabase Storage | 🔜 Coming Soon | PostgreSQL-backed storage |
| Vercel Blob | 🔜 Coming Soon | Edge-optimized storage |

## Module Structure

```
storage/
├── __init__.py         # Package initialization
├── base.py            # Abstract base storage class
├── s3.py              # S3-compatible storage backends
├── factory.py         # Factory for selecting storage backend
└── utils.py           # Helper utilities
```

## Storage Classes

### S3MediaStorage

Public storage for user-uploaded files (avatars, event images, etc.):

```python
from django.db import models
from storage.s3 import S3MediaStorage

class Profile(models.Model):
    avatar = models.ImageField(storage=S3MediaStorage())
```

**Features:**
- Public read access
- Unique filenames (no overwrites)
- CDN support

### S3PrivateStorage

Private storage for sensitive files:

```python
from storage.s3 import S3PrivateStorage

class Invoice(models.Model):
    file = models.FileField(storage=S3PrivateStorage())
```

**Features:**
- Private access only
- Pre-signed URLs (1 hour expiry)
- No CDN

### S3StaticStorage

For static files (CSS, JS):

```python
# In settings.py
STATICFILES_STORAGE = "storage.s3.S3StaticStorage"
```

## Configuration

All configuration is done via environment variables in `.env`:

```bash
# Storage Backend Selection
STORAGE_BACKEND=s3  # Options: local, s3, minio

# S3 Configuration
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Optional: Custom endpoint (for MinIO, DigitalOcean Spaces, etc.)
AWS_S3_ENDPOINT_URL=http://localhost:9000

# Optional: SSL (disable for local MinIO)
AWS_S3_USE_SSL=True

# Optional: CDN domain
AWS_S3_CUSTOM_DOMAIN=cdn.example.com

# Optional: Use S3 for static files
USE_S3_FOR_STATIC=False
```

See `.env.example` for all available options.

## Usage Examples

### Default (Let Django Choose)

By default, models use the configured storage backend:

```python
class Profile(models.Model):
    # Uses DEFAULT_FILE_STORAGE from settings
    avatar = models.ImageField(upload_to="avatars/")
```

### Explicit Storage Backend

Specify storage backend per field:

```python
from storage.s3 import S3MediaStorage, S3PrivateStorage

class Event(models.Model):
    # Public files
    banner = models.ImageField(storage=S3MediaStorage())
    
    # Private files
    attendee_list = models.FileField(storage=S3PrivateStorage())
```

### Factory Pattern

Get storage backend programmatically:

```python
from storage.factory import get_media_storage, get_private_storage

# Get configured media storage
media_storage = get_media_storage()

# Get private storage
private_storage = get_private_storage()
```

### Custom Upload Paths

Use utility functions for organized file paths:

```python
from storage.utils import generate_avatar_path

class Profile(models.Model):
    avatar = models.ImageField(upload_to=generate_avatar_path)
```

## Documentation

- [Storage Overview](../docs/storage/overview.md) - Architecture and design
- [MinIO Setup](../docs/storage/minio.md) - Local development setup
- [Migration Guide](../docs/storage/overview.md#migration-guide) - Switch between providers

## Troubleshooting

### Files not uploading

1. Check credentials in `.env`
2. Verify bucket exists
3. Check bucket permissions (public-read for media)
4. Verify network connectivity

### URLs not working

1. Check `AWS_S3_CUSTOM_DOMAIN` setting
2. Verify bucket has public read permissions
3. Check CORS configuration (for web uploads)

### "Access Denied" errors

1. Verify IAM permissions
2. Check bucket policy
3. Ensure credentials are correct

## Testing

```bash
# Run Django checks
python manage.py check

# Test storage import
python -c "from storage import get_storage_backend; print('✓ OK')"

# Test file upload (through Django admin or web interface)
python manage.py runserver
# Go to http://localhost:8000/profile and upload an avatar
```

## Security Best Practices

1. **Never commit credentials** - Use `.env` file (gitignored)
2. **Use IAM roles** - In AWS, prefer IAM roles over access keys
3. **Restrict permissions** - Only grant necessary S3 permissions
4. **Enable versioning** - Protect against accidental deletions
5. **Use HTTPS** - Always use SSL in production (`AWS_S3_USE_SSL=True`)
6. **Rotate keys** - Regularly rotate access keys

## Future Providers

The storage system is designed to easily add new providers:

- **Supabase Storage** - Coming soon
- **Vercel Blob** - Coming soon
- **Google Cloud Storage** - Planned
- **Azure Blob Storage** - Planned

## Contributing

To add a new storage provider:

1. Create a new file `storage/{provider}.py`
2. Implement storage backend class
3. Update `factory.py` to include new provider
4. Add documentation in `docs/storage/{provider}.md`
5. Update this README

## Support

For issues or questions:
- Check the [documentation](../docs/storage/)
- Review [technical quirks](../docs/technical_quirks.md)
- Open an issue on GitHub
