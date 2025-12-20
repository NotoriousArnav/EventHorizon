# MinIO Setup Guide

MinIO is an open-source, S3-compatible object storage server perfect for local development. This guide will help you set up MinIO for EventHorizon.

## Why MinIO?

- **S3-Compatible**: Works exactly like AWS S3
- **Local Development**: No cloud costs during development
- **Fast**: Run locally on your machine
- **Easy Setup**: Docker or standalone binary
- **Production Ready**: Can be used in production too

## Prerequisites

- Docker (recommended) or MinIO binary
- EventHorizon project set up

## Installation

### Option 1: Docker (Recommended)

#### 1. Run MinIO with Docker

```bash
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -v ~/minio/data:/data \
  quay.io/minio/minio server /data --console-address ":9001"
```

**Explanation:**
- `-p 9000:9000` - API endpoint
- `-p 9001:9001` - Web console
- `-v ~/minio/data:/data` - Persist data to your home directory
- `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` - Admin credentials

#### 2. Verify MinIO is Running

Open your browser and go to: http://localhost:9001

Login with:
- **Username**: `minioadmin`
- **Password**: `minioadmin`

### Option 2: Docker Compose

Create a `docker-compose.yml` file in your project root:

```yaml
version: '3.8'

services:
  minio:
    image: quay.io/minio/minio
    container_name: eventhorizon-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

volumes:
  minio_data:
    driver: local
```

Start MinIO:

```bash
docker-compose up -d minio
```

### Option 3: Standalone Binary

#### macOS

```bash
brew install minio/stable/minio
minio server ~/minio/data --console-address ":9001"
```

#### Linux

```bash
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
./minio server ~/minio/data --console-address ":9001"
```

#### Windows

Download from: https://dl.min.io/server/minio/release/windows-amd64/minio.exe

```powershell
.\minio.exe server C:\minio\data --console-address ":9001"
```

## Configuration

### 1. Create a Bucket

**Via Web Console:**

1. Open http://localhost:9001
2. Login with `minioadmin` / `minioadmin`
3. Click "Buckets" → "Create Bucket"
4. Bucket Name: `eventhorizon`
5. Click "Create Bucket"

**Via MinIO Client (mc):**

```bash
# Install mc
brew install minio/stable/mc  # macOS
# or download from https://min.io/docs/minio/linux/reference/minio-mc.html

# Configure mc
mc alias set local http://localhost:9000 minioadmin minioadmin

# Create bucket
mc mb local/eventhorizon

# Set public read policy for media files
mc anonymous set download local/eventhorizon/media
```

### 2. Configure EventHorizon

Update your `.env` file:

```bash
# Storage Configuration
STORAGE_BACKEND=minio

# MinIO Configuration
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_STORAGE_BUCKET_NAME=eventhorizon
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_S3_USE_SSL=False
AWS_S3_REGION_NAME=us-east-1
```

### 3. Test the Configuration

```bash
# Start Django development server
python manage.py runserver

# Go to http://localhost:8000/profile
# Upload a profile picture
# The file should be stored in MinIO
```

### 4. Verify File Upload

**Via Web Console:**

1. Open http://localhost:9001
2. Navigate to Buckets → eventhorizon → media → avatars
3. You should see your uploaded files

**Via Browser:**

The uploaded file should be accessible at:
```
http://localhost:9000/eventhorizon/media/avatars/users/{user_id}/{file_name}
```

## Bucket Policy Configuration

To make files publicly readable, set the bucket policy:

**Via Web Console:**

1. Go to Buckets → eventhorizon
2. Click "Manage" → "Access Rules"
3. Add a rule:
   - Prefix: `media/*`
   - Access: `readonly`

**Via MinIO Client:**

```bash
# Create a policy file
cat > /tmp/policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": ["*"]},
      "Action": ["s3:GetObject"],
      "Resource": ["arn:aws:s3:::eventhorizon/media/*"]
    }
  ]
}
EOF

# Apply the policy
mc anonymous set-json /tmp/policy.json local/eventhorizon
```

## CORS Configuration

If you're uploading files from a web frontend, configure CORS:

**Via MinIO Client:**

```bash
cat > /tmp/cors.json <<EOF
{
  "CORSRules": [
    {
      "AllowedOrigins": ["http://localhost:8000", "http://localhost:3000"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"]
    }
  ]
}
EOF

mc cors set /tmp/cors.json local/eventhorizon
```

## Production Considerations

### Using MinIO in Production

MinIO can be used in production! Here's how to make it production-ready:

#### 1. Use Strong Credentials

```bash
# Generate strong credentials
MINIO_ROOT_USER=$(openssl rand -hex 20)
MINIO_ROOT_PASSWORD=$(openssl rand -hex 32)

# Set in docker-compose.yml or as environment variables
```

#### 2. Enable TLS

```bash
# Generate certificates or use Let's Encrypt
docker run -d \
  --name minio \
  -p 9000:9000 \
  -p 9001:9001 \
  -v ~/minio/data:/data \
  -v ~/minio/certs:/root/.minio/certs \
  -e MINIO_ROOT_USER=${MINIO_ROOT_USER} \
  -e MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD} \
  quay.io/minio/minio server /data --console-address ":9001"

# Update .env
AWS_S3_ENDPOINT_URL=https://minio.yourdomain.com
AWS_S3_USE_SSL=True
```

#### 3. Set Up Replication (Optional)

For high availability:

```bash
# Set up distributed MinIO with multiple nodes
docker run -d \
  --name minio1 \
  quay.io/minio/minio server \
  http://minio{1...4}/data --console-address ":9001"
```

#### 4. Use a Reverse Proxy

Configure Nginx or Caddy to proxy MinIO:

```nginx
# Nginx configuration
server {
    listen 80;
    server_name minio.yourdomain.com;

    location / {
        proxy_pass http://localhost:9000;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Large file uploads
        client_max_body_size 100M;
    }
}
```

## Troubleshooting

### Connection Refused

**Problem**: Can't connect to MinIO at http://localhost:9000

**Solutions**:
1. Verify MinIO is running:
   ```bash
   docker ps | grep minio
   # or
   curl http://localhost:9000/minio/health/live
   ```

2. Check port conflicts:
   ```bash
   lsof -i :9000
   ```

3. Check Docker logs:
   ```bash
   docker logs minio
   ```

### Access Denied Errors

**Problem**: Files upload but can't be accessed

**Solutions**:
1. Check bucket policy (see Bucket Policy Configuration above)
2. Verify credentials in `.env`
3. Make sure bucket name matches in settings

### Files Not Showing in MinIO Console

**Problem**: Files upload successfully but don't appear in console

**Solutions**:
1. Refresh the page
2. Check the correct bucket path: `media/avatars/users/`
3. Verify `STORAGE_BACKEND=minio` in `.env`

### SSL Certificate Errors

**Problem**: SSL errors when using custom domain

**Solutions**:
1. Use `AWS_S3_USE_SSL=False` for local development
2. For production, ensure valid SSL certificates
3. Check `AWS_S3_ENDPOINT_URL` format

## Advanced Usage

### Multiple Buckets

Use different buckets for different purposes:

```python
# In your models
from storage.s3 import S3MediaStorage

class CustomStorage(S3MediaStorage):
    bucket_name = 'eventhorizon-events'

class Event(models.Model):
    banner = models.ImageField(storage=CustomStorage())
```

### Image Processing

Integrate with MinIO's image processing:

```python
# settings.py
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
```

### Backup and Restore

```bash
# Backup
mc mirror local/eventhorizon /backup/minio/

# Restore
mc mirror /backup/minio/ local/eventhorizon
```

## Next Steps

- [Overview](./overview.md) - Storage system architecture
- [AWS S3 Setup](./aws-s3.md) - Migrate to AWS S3 for production
- [S3-Compatible Providers](./s3-compatible.md) - Other alternatives

## Resources

- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
- [MinIO Client (mc) Guide](https://min.io/docs/minio/linux/reference/minio-mc.html)
- [Django-Storages Documentation](https://django-storages.readthedocs.io/)
