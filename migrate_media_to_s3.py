#!/usr/bin/env python
# Event Horizon - Futuristic Event Management Platform
# Copyright (C) 2025-2026 Arnav Ghosh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""
Migrate existing media files from local filesystem to S3-compatible storage.

Usage:
    python migrate_media_to_s3.py [--dry-run] [--delete-local]

Options:
    --dry-run       Show what would be migrated without actually uploading
    --delete-local  Delete local files after successful migration
"""

import os
import sys
import argparse
from pathlib import Path

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EventHorizon.settings")
import django

django.setup()

from django.conf import settings
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError


def get_s3_client():
    """Get configured S3 client."""
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
        region_name=settings.AWS_S3_REGION_NAME,
        use_ssl=settings.AWS_S3_USE_SSL,
    )


def get_content_type(file_path):
    """Determine content type from file extension."""
    import mimetypes

    content_type, _ = mimetypes.guess_type(str(file_path))
    return content_type or "application/octet-stream"


def migrate_files(dry_run=False, delete_local=False):
    """Migrate all files from local media directory to S3."""

    # Check if S3 is configured
    if settings.STORAGE_BACKEND not in ["s3", "minio"]:
        print('❌ Error: STORAGE_BACKEND must be set to "s3" or "minio"')
        print("   Update your .env file and try again.")
        return False

    # Get media root
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        # If MEDIA_ROOT not set, we're already using S3
        print("✓ Already using S3 storage, no local files to migrate")
        return True

    media_root = Path(media_root)
    if not media_root.exists():
        print("✓ No local media directory found, nothing to migrate")
        return True

    # Get S3 client
    try:
        s3 = get_s3_client()
        bucket = settings.AWS_STORAGE_BUCKET_NAME
    except Exception as e:
        print(f"❌ Error connecting to S3: {e}")
        return False

    # Find all files
    files_to_migrate = []
    for file_path in media_root.rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(media_root)
            files_to_migrate.append((file_path, relative_path))

    if not files_to_migrate:
        print("✓ No files to migrate")
        return True

    print(
        f"\n{'🔍 DRY RUN - ' if dry_run else ''}Found {len(files_to_migrate)} file(s) to migrate:\n"
    )

    # Migrate each file
    success_count = 0
    error_count = 0

    for local_path, relative_path in files_to_migrate:
        s3_key = f"media/{relative_path.as_posix()}"

        print(f"📤 {relative_path}")
        print(f"   Local: {local_path}")
        print(f"   S3 Key: {s3_key}")

        if dry_run:
            print(f"   [DRY RUN] Would upload to s3://{bucket}/{s3_key}")
            success_count += 1
            print()
            continue

        try:
            # Check if file already exists in S3
            try:
                s3.head_object(Bucket=bucket, Key=s3_key)
                print(f"   ⚠️  Already exists in S3, skipping")
                success_count += 1
                print()
                continue
            except ClientError:
                pass  # File doesn't exist, proceed with upload

            # Upload file
            file_size = local_path.stat().st_size
            content_type = get_content_type(local_path)

            with open(local_path, "rb") as f:
                s3.put_object(
                    Bucket=bucket,
                    Key=s3_key,
                    Body=f,
                    ContentType=content_type,
                    ACL="public-read",
                )

            # Verify upload
            s3.head_object(Bucket=bucket, Key=s3_key)
            print(f"   ✅ Uploaded ({file_size:,} bytes)")

            # Delete local file if requested
            if delete_local:
                local_path.unlink()
                print(f"   🗑️  Deleted local file")

            success_count += 1

        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1

        print()

    # Summary
    print("─" * 60)
    print(f"\n{'DRY RUN - ' if dry_run else ''}Migration Summary:")
    print(f"  ✅ Successful: {success_count}")
    if error_count > 0:
        print(f"  ❌ Failed: {error_count}")
    print()

    if not dry_run and success_count > 0:
        # List files in S3
        print("📋 Files now in S3:")
        response = s3.list_objects_v2(Bucket=bucket, Prefix="media/")
        if "Contents" in response:
            for obj in response["Contents"]:
                print(f"  ✓ {obj['Key']} ({obj['Size']:,} bytes)")
        print()

    return error_count == 0


def main():
    parser = argparse.ArgumentParser(
        description="Migrate local media files to S3 storage"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without uploading",
    )
    parser.add_argument(
        "--delete-local",
        action="store_true",
        help="Delete local files after successful migration",
    )

    args = parser.parse_args()

    print("🚀 EventHorizon Media Migration Tool")
    print("─" * 60)

    if args.dry_run:
        print("ℹ️  Running in DRY RUN mode - no files will be uploaded")

    if args.delete_local and not args.dry_run:
        print("⚠️  WARNING: Local files will be deleted after migration")
        response = input("Continue? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("Cancelled.")
            return

    print()

    success = migrate_files(dry_run=args.dry_run, delete_local=args.delete_local)

    if success:
        print("✅ Migration completed successfully!")
        if not args.dry_run and not args.delete_local:
            print("\nℹ️  Local files are still present. To remove them:")
            print("   python migrate_media_to_s3.py --delete-local")
    else:
        print("❌ Migration completed with errors")
        sys.exit(1)


if __name__ == "__main__":
    main()
