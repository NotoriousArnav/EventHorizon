# Dependencies and Licenses

This document provides an overview of Event Horizon's third-party dependencies and their licenses.

## Table of Contents

- [Introduction](#introduction)
- [License Compatibility](#license-compatibility)
- [Core Dependencies](#core-dependencies)
- [Development Dependencies](#development-dependencies)
- [JavaScript Dependencies](#javascript-dependencies)
- [Transitive Dependencies](#transitive-dependencies)
- [License Auditing](#license-auditing)

## Introduction

Event Horizon is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. This document lists all major third-party dependencies and their respective licenses.

### Why This Matters

Understanding the licenses of our dependencies is important because:

- **Legal Compliance:** Ensures we respect the terms of each dependency's license
- **GPL Compatibility:** All dependencies must be compatible with GPL-3.0
- **Transparency:** Users and contributors should know what licenses apply to the software
- **Trust:** Demonstrates our commitment to open source principles

## License Compatibility

All dependencies used in Event Horizon are compatible with GPL-3.0. The following license types are included:

- **BSD Licenses (BSD-3-Clause, BSD-2-Clause):** Permissive licenses compatible with GPL
- **MIT License:** Permissive license compatible with GPL
- **Apache License 2.0:** Permissive license compatible with GPL
- **LGPL-3.0:** Lesser GPL, compatible with GPL-3.0
- **HPND (Historical Permission Notice and Disclaimer):** Permissive license compatible with GPL

### GPL-3.0 Compatibility

The GPL-3.0 license allows:
- Using libraries under more permissive licenses (MIT, BSD, Apache)
- Linking with LGPL libraries
- Combining with other GPL-compatible free software

The GPL-3.0 license does NOT allow:
- Linking with proprietary software (without special exceptions)
- Using dependencies under incompatible copyleft licenses

## Core Dependencies

These are the essential Python packages Event Horizon depends on:

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **Django** | ≥6.0 | BSD-3-Clause | Web framework |
| **django-allauth** | ≥65.13.1 | MIT | Authentication and social auth |
| **django-oauth-toolkit** | latest | BSD-2-Clause | OAuth2 provider |
| **djangorestframework** | latest | BSD-3-Clause | REST API framework |
| **django-rest-knox** | ≥5.0.2 | MIT | Token authentication |
| **django-cors-headers** | ≥4.9.0 | MIT | CORS handling |
| **django-storages** | ≥1.14.4 | BSD-3-Clause | Storage backends |
| **django-filter** | latest | BSD-3-Clause | Filtering for DRF |
| **Pillow** | ≥12.0.0 | HPND | Image processing |
| **psycopg2** | ≥2.9.11 | LGPL-3.0 | PostgreSQL adapter |
| **boto3** | ≥1.35.0 | Apache-2.0 | AWS SDK for S3 storage |
| **requests** | ≥2.31.0 | Apache-2.0 | HTTP library |
| **gunicorn** | ≥21.2.0 | MIT | WSGI HTTP server |
| **whitenoise** | ≥6.6.0 | MIT | Static file serving |
| **python-dotenv** | ≥1.2.1 | BSD-3-Clause | Environment variable management |
| **cryptography** | ≥46.0.3 | Apache-2.0/BSD | Cryptographic operations |
| **dj-database-url** | ≥3.0.1 | BSD-2-Clause | Database URL parsing |
| **markdown** | latest | BSD-3-Clause | Markdown rendering |
| **tzdata** | ≥2025.2 | Apache-2.0 | Timezone data |

### License Details

#### BSD-3-Clause (Django, DRF, django-storages, django-filter, python-dotenv, markdown)

The 3-Clause BSD License is a permissive license that allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Include copyright notice
- Include license text

#### MIT (django-allauth, knox, cors-headers, gunicorn, whitenoise)

The MIT License is a very permissive license that allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Include copyright notice
- Include license text

#### Apache-2.0 (boto3, requests, cryptography, tzdata)

The Apache License 2.0 is a permissive license that allows:
- Commercial use
- Modification
- Distribution
- Patent use
- Private use

Requirements:
- Include copyright notice
- Include license text
- State changes
- Include NOTICE file if present

#### LGPL-3.0 (psycopg2)

The GNU Lesser General Public License allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Source code must be disclosed for LGPL portions
- Include copyright notice
- Include license text
- State changes

Note: LGPL allows linking from non-GPL software, making it more permissive than GPL while still being copyleft.

#### HPND (Pillow)

The Historical Permission Notice and Disclaimer is a permissive license similar to BSD that allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Include copyright notice
- Include license text

## Development Dependencies

These dependencies are only used during development and testing:

| Package | Version | License | Purpose |
|---------|---------|---------|---------|
| **pytest** | ≥7.4.0 | MIT | Testing framework |
| **pytest-django** | ≥4.5.0 | BSD-3-Clause | Django plugin for pytest |

## JavaScript Dependencies

Frontend dependencies managed via npm:

| Package | License | Purpose |
|---------|---------|---------|
| **tailwindcss** | MIT | CSS framework |
| **@tailwindcss/forms** | MIT | Form styling |
| **autoprefixer** | MIT | CSS vendor prefixing |
| **postcss** | MIT | CSS processing |

All JavaScript dependencies use the MIT License, which is GPL-compatible.

## Transitive Dependencies

### What Are Transitive Dependencies?

Transitive dependencies are packages that our direct dependencies rely on. For example:
- Django depends on `asgiref` and `sqlparse`
- boto3 depends on `botocore` and `jmespath`
- djangorestframework depends on Django

### License Inheritance

Our direct dependencies (listed above) have their own dependencies, which may have different licenses. However:

1. **Our direct dependencies handle compatibility:** Package maintainers ensure their dependencies are compatible with their own license.

2. **Verification:** We periodically audit transitive dependencies to ensure no incompatible licenses are introduced.

3. **Common transitive licenses:**
   - Most use MIT, BSD, or Apache licenses
   - All are GPL-3.0 compatible

### Example Dependency Tree

```
Event Horizon (GPL-3.0)
├── Django (BSD-3-Clause)
│   ├── asgiref (BSD-3-Clause)
│   ├── sqlparse (BSD-3-Clause)
│   └── tzdata (Apache-2.0)
├── boto3 (Apache-2.0)
│   ├── botocore (Apache-2.0)
│   ├── jmespath (MIT)
│   └── s3transfer (Apache-2.0)
└── Pillow (HPND)
    └── (C extensions, same license)
```

## License Auditing

### How to Audit Dependencies

You can verify the licenses of all installed dependencies using these tools:

#### Using pip-licenses

```bash
# Install pip-licenses
pip install pip-licenses

# Show all licenses
pip-licenses

# Export to CSV
pip-licenses --format=csv --output-file=licenses.csv

# Show only certain formats
pip-licenses --format=markdown

# Filter by license
pip-licenses --filter-strings="MIT;BSD;Apache"
```

#### Using pip show

```bash
# Check a specific package
pip show django

# Output includes license information:
# Name: Django
# Version: 6.0
# License: BSD-3-Clause
```

#### Using uv (if installed)

```bash
# Show dependency tree
uv pip list --format=tree

# Show package details
uv pip show django
```

### Checking for License Changes

When updating dependencies:

```bash
# Before updating
pip-licenses --format=csv --output-file=licenses-before.csv

# Update dependencies
uv sync --upgrade

# After updating
pip-licenses --format=csv --output-file=licenses-after.csv

# Compare
diff licenses-before.csv licenses-after.csv
```

### Red Flags to Watch For

When auditing dependencies, be cautious of:

- **Proprietary licenses:** Should never appear in our dependencies
- **GPL-incompatible licenses:** Such as older versions of OpenSSL license
- **Unknown licenses:** Packages without clear license information
- **License changes:** Dependencies that change licenses between versions

### Automated Auditing

Consider setting up automated license checking in CI/CD:

```bash
# In your CI pipeline
pip install pip-licenses
pip-licenses --fail-on="GPL-2.0;Proprietary"  # Fails if incompatible licenses found
```

## License Compliance

### For Users

When you use Event Horizon:

1. **GPL-3.0 applies:** The entire application is licensed under GPL-3.0
2. **Source code availability:** You have the right to access and modify all source code
3. **Distribution terms:** If you distribute modified versions, you must:
   - Provide source code
   - License under GPL-3.0
   - Include copyright notices

### For Developers

When contributing to Event Horizon:

1. **Check dependency licenses:** Before adding new dependencies, verify GPL compatibility
2. **Document new dependencies:** Update this file when adding dependencies
3. **Avoid incompatible licenses:** Do not add dependencies with GPL-incompatible licenses
4. **Consider license obligations:** Some licenses (like Apache 2.0) require preserving NOTICE files

### For Distributors

If you distribute Event Horizon:

1. **Include LICENSE:** The GPL-3.0 license file must be included
2. **Include this file:** DEPENDENCIES.md should be included for transparency
3. **Provide source code:** You must make source code available to recipients
4. **Preserve notices:** Keep all copyright and license notices intact
5. **Document modifications:** Clearly state if you've modified the code

## Additional Resources

### License Texts

- **GPL-3.0:** See the LICENSE file in the repository root
- **Other licenses:** Check the LICENSE file in each dependency's source

### Further Reading

- [GPL-3.0 Official Text](https://www.gnu.org/licenses/gpl-3.0.html)
- [GPL-3.0 FAQ](https://www.gnu.org/licenses/gpl-faq.html)
- [GPL Compatibility](https://www.gnu.org/licenses/license-compatibility.html)
- [SPDX License List](https://spdx.org/licenses/)
- [Choose a License](https://choosealicense.com/)

### Tools

- [pip-licenses](https://github.com/raimon49/pip-licenses) - License checker for Python packages
- [license-checker](https://github.com/davglass/license-checker) - License checker for npm packages
- [FOSSA](https://fossa.com/) - Automated license compliance
- [WhiteSource](https://www.whitesourcesoftware.com/) - Open source security and license compliance

## Questions?

If you have questions about:
- **Licensing:** See the LICENSE file or consult the GPL-3.0 FAQ
- **Compatibility:** Check the GPL compatibility matrix
- **Contributing:** See CONTRIBUTING.md
- **Specific dependencies:** Check the package's own license file

## Updates

This document should be updated whenever:
- New dependencies are added
- Dependencies are removed
- Major version updates occur that might change licenses
- License compliance requirements change

**Last Updated:** December 21, 2025

---

**Note:** While we strive to keep this document accurate and up-to-date, the license information in each package's own metadata is authoritative. Always verify license information when in doubt.
