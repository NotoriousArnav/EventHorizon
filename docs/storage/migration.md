# S3 Storage Testing Summary

## Issue Encountered

When accessing files uploaded before S3 configuration, received error:
```xml
<Error>
  <Code>NoSuchKey</Code>
  <Message>The specified key does not exist.</Message>
</Error>
```

## Root Cause

Files uploaded to the local filesystem **before** configuring S3 storage remained in the local `media/` directory. After switching to S3, Django generated URLs pointing to MinIO, but the files weren't there.

## Solution Implemented

### 1. File Migration Script (`migrate_media_to_s3.py`)

Created a comprehensive migration tool that:
- ✅ Detects all files in local `media/` directory
- ✅ Uploads them to S3/MinIO with proper structure
- ✅ Sets correct content types and permissions
- ✅ Supports dry-run mode for testing
- ✅ Optional local file cleanup after migration
- ✅ Skips already-uploaded files

### 2. Manual Migration Performed

Successfully migrated existing files:
- `avatars/Screenshot_From_2025-12-14_22-16-22.png` (190,633 bytes) ✅
- Verified public accessibility via HTTP

### 3. Testing & Verification

All tests passed:
```
✅ arnav's avatar: HTTP 200 - Accessible (190,633 bytes)
✅ miniotest's avatar: HTTP 200 - Accessible (1,029 bytes)
```

## How to Prevent This Issue

### For New Deployments

1. **Configure S3 BEFORE first use**:
   ```bash
   # Set in .env before running server
   STORAGE_BACKEND=minio
   AWS_ACCESS_KEY_ID=...
   # etc.
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create S3 bucket** with proper permissions

4. **Test with a file upload**

### For Existing Deployments

If you already have local files, migrate them:

```bash
# 1. Configure S3 in .env
STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=...

# 2. Test migration (dry run)
python migrate_media_to_s3.py --dry-run

# 3. Perform actual migration
python migrate_media_to_s3.py

# 4. Optionally clean up local files
python migrate_media_to_s3.py --delete-local
```

## File Storage Structure

Files in MinIO/S3 are stored with this structure:
```
bucket-name/
└── media/
    └── avatars/
        ├── Screenshot_From_2025-12-14_22-16-22.png
        └── minio_test.jpg
```

URLs are generated as:
```
http://localhost:9000/eventhorizon/media/avatars/filename.jpg
```

## Troubleshooting

### Issue: "NoSuchKey" error

**Cause**: File not in S3, still in local filesystem

**Solution**: Run migration script
```bash
python migrate_media_to_s3.py
```

### Issue: "Access Denied" error

**Cause**: Bucket policy not configured for public read

**Solution**: Set bucket policy (automatically done by migration script)

### Issue: File uploads work but old files don't

**Cause**: Old files uploaded before S3 configuration

**Solution**: Migrate files using the migration script

## Testing Checklist

After configuring S3 storage:

- [ ] Django system check passes
- [ ] Can upload new files via web interface
- [ ] New files appear in MinIO bucket
- [ ] New file URLs are accessible (HTTP 200)
- [ ] Existing files migrated (if applicable)
- [ ] Old file URLs work (if applicable)

## Production Recommendations

1. **Always test migration in staging first**
2. **Backup local media directory** before deletion
3. **Use `--dry-run` first** to preview migration
4. **Verify all files accessible** after migration
5. **Keep local backups** for at least 7 days
6. **Monitor error logs** for 404s on file URLs

## Migration Command Reference

```bash
# See what would be migrated
python migrate_media_to_s3.py --dry-run

# Migrate files (keep local copies)
python migrate_media_to_s3.py

# Migrate and delete local files
python migrate_media_to_s3.py --delete-local

# Get help
python migrate_media_to_s3.py --help
```
