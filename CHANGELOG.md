# Changelog

All notable changes to Event Horizon will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Local Tailwind CSS setup with build pipeline (npm scripts)
- Dynamic "Add Social Link" functionality with JavaScript
- Comprehensive storage documentation (4 guides)
- `DEPLOYMENT.md` and `DEVELOPMENT.md` guides
- Email configuration documentation
- Automated Tailwind CSS build and watch scripts
- Custom formset validation for empty social link forms
- Event utility functions in `events/utils.py`

### Changed
- Replaced Tailwind CSS CDN with local compiled CSS (41KB minified)
- Profile form validation now only shows on POST requests
- Social link formset now uses `extra=0` to prevent empty form validation errors
- Made social link platform and URL fields optional with custom validation
- Updated init_project.py to include Node.js and Tailwind CSS setup
- Improved event slug generation with retry logic and UUID fallback
- Enhanced error messages display in profile template

### Fixed
- Profile upload UI validation errors showing on page load
- Social link formset validation requiring empty extra forms
- Static files 404 errors by adding STATICFILES_DIRS
- Form error display logic to check request method
- Delete checkbox now shows for all social links (not just existing ones)

### Removed
- Tailwind CSS CDN dependency (performance improvement)
- CDN configuration JavaScript from base template
- Debug print statements from user views

## [0.2.0] - 2025-12-20

### Added
- S3-compatible storage system supporting multiple providers:
  - AWS S3
  - MinIO
  - DigitalOcean Spaces
  - Cloudflare R2
  - Backblaze B2
  - Supabase Storage (planned)
  - Vercel Blob (planned)
- Factory pattern for storage backend selection
- Three storage classes: public media, static files, private files
- Automated migration script (`migrate_media_to_s3.py`)
- Django 6.0 STORAGES configuration
- Comprehensive storage documentation
- Profile image upload UI with visual feedback
- File format and size hints for avatar uploads
- Django messages display in profile template

### Changed
- Updated to Django 6.0 STORAGES dict (not deprecated DEFAULT_FILE_STORAGE)
- Profile template UI improvements with better error handling
- File input styling with orange button theme

### Fixed
- Profile image upload only working from Django Admin
- NoSuchKey errors for files uploaded before S3 configuration
- Form validation errors not displaying to users
- Missing visual feedback on profile updates

## [0.1.0] - 2024-12-XX

### Added
- Event management platform with custom registration schemas
- OAuth2/OpenID Connect support (RS256 signing)
- User profile system with avatars and social links
- Event CRUD operations with slug generation
- Event registration with custom JSON schemas
- Data visualization and CSV export
- RESTful API with Django REST Framework
- PHP OAuth2 client example
- Vanilla PHP Event Manager Client (SPA)
- GitHub Actions CI/CD workflow
- Comprehensive documentation with Jekyll theme
- Project initialization script
- Custom user authentication

### Technical Stack
- Django 6.0
- Python 3.12
- OAuth2 Provider
- Django Allauth
- Django REST Framework
- Tailwind CSS
- SQLite (default) / PostgreSQL support
- Boto3 for S3 storage

---

## Release Notes

### Performance Improvements
- **v0.2.0**: Local Tailwind CSS reduces page load time by eliminating CDN requests
- **v0.2.0**: S3 storage offloads media serving from application server

### Breaking Changes
- **v0.2.0**: Requires environment variables for S3 configuration (see `.env.example`)
- **v0.1.0**: Requires Python 3.12+

### Migration Guide
- **To v0.2.0**: Run `python migrate_media_to_s3.py --dry-run` to preview media migration
- **To v0.2.0**: Install Node.js dependencies: `npm install`
- **To v0.2.0**: Build Tailwind CSS: `npm run build:css`

---

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/NotoriousArnav/EventHorizon/tags).

## Links

- [GitHub Repository](https://github.com/NotoriousArnav/EventHorizon)
- [Documentation](https://notoriousarnav.github.io/EventHorizon/)
- [Issue Tracker](https://github.com/NotoriousArnav/EventHorizon/issues)
