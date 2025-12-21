# Contributing to Event Horizon

Welcome! We're excited that you're interested in contributing to Event Horizon. This document outlines the guidelines for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [License and Copyright](#license-and-copyright)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Reporting Issues](#reporting-issues)
- [Contact](#contact)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## License and Copyright

### License

Event Horizon is licensed under the **GNU General Public License v3.0 (GPL-3.0)**. This is a copyleft license that requires anyone who distributes your code or a derivative work to make the source available under the same terms.

### Contributor Agreement

By submitting a contribution to Event Horizon, you agree to the following terms:

1. **License Grant:** You grant the project maintainers and all users a perpetual, worldwide, non-exclusive, royalty-free license to your contribution under the GPL-3.0 license.

2. **Original Work:** You certify that your contribution is your original work or that you have the right to submit it under the GPL-3.0 license.

3. **GPL-3.0 Compliance:** You understand that all contributions will be licensed under GPL-3.0, and any derivative works must also be licensed under GPL-3.0.

4. **No Warranty:** As per GPL-3.0 terms, contributions are provided "as is" without warranty of any kind.

5. **Attribution:** You agree that your contributions may be attributed to you through git commit history and other project records.

### What This Means

- All contributions become part of the GPL-3.0 licensed codebase
- Anyone can use, modify, and distribute the code under GPL-3.0 terms
- If someone distributes modified versions, they must also release their source code under GPL-3.0
- You retain copyright to your contributions, but license them under GPL-3.0

## Getting Started

Before you begin:

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Set up your development environment** (see below)
4. **Create a branch** for your changes

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Node.js (for Tailwind CSS)
- Git
- uv package manager (recommended) or pip

### Quick Setup

The fastest way to get started is using our automated build script:

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/EventHorizon.git
cd EventHorizon

# Run automated setup
./build.sh

# Configure environment
python init_project.py
```

### Manual Setup

If you prefer manual setup:

1. **Install uv package manager:**
   ```bash
   # macOS / Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Install Python dependencies:**
   ```bash
   uv sync
   ```

3. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

4. **Build Tailwind CSS:**
   ```bash
   npm run build:css
   ```

5. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

### Running the Development Server

```bash
# Start Django development server
uv run python manage.py runserver

# In another terminal, watch for CSS changes
npm run watch:css
```

Access the application at http://127.0.0.1:8000

## Code Style Guidelines

### Python Code Style

We follow PEP 8 with some project-specific conventions:

1. **Formatting:**
   - Use 4 spaces for indentation (no tabs)
   - Maximum line length: 100 characters
   - Use blank lines to separate logical sections

2. **Naming Conventions:**
   - Classes: `PascalCase`
   - Functions/methods: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private methods: `_leading_underscore`

3. **Imports:**
   - Group imports: standard library, third-party, local
   - Use absolute imports when possible
   - One import per line

4. **Documentation:**
   - All public modules, classes, and functions should have docstrings
   - Use clear, descriptive variable names
   - Comment complex logic

Example:
```python
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    Represents an event with registration and attendance tracking.
    """
    title = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def approve_registration(self, registration):
        """
        Approve a pending registration and send confirmation email.
        
        Args:
            registration: The Registration object to approve
            
        Returns:
            bool: True if approval was successful
        """
        # Implementation here
        pass
```

### JavaScript/CSS

1. **JavaScript:**
   - Use modern ES6+ syntax
   - Use `const` and `let`, avoid `var`
   - Use meaningful variable names

2. **Tailwind CSS:**
   - Use utility classes from tailwind.config.js
   - Follow the project's design system
   - Maintain the "Command Terminal" aesthetic

### Django-Specific Guidelines

1. **Models:**
   - Use descriptive field names
   - Add help_text for clarity
   - Override `__str__()` method
   - Add Meta class with ordering

2. **Views:**
   - Use class-based views when appropriate
   - Add permission checks
   - Handle errors gracefully

3. **Templates:**
   - Extend base.html
   - Use template tags appropriately
   - Keep logic in views, not templates

4. **API:**
   - Follow REST principles
   - Use appropriate HTTP methods
   - Return proper status codes
   - Document endpoints

## Making Changes

### Workflow

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write clean, readable code
   - Follow style guidelines
   - Add/update tests
   - Update documentation if needed

3. **Test your changes:**
   ```bash
   # Run tests
   python manage.py test
   
   # Check for issues
   python manage.py check
   
   # Test migrations
   python manage.py makemigrations --dry-run
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```
   
   Use clear commit messages:
   - Start with a verb (Add, Fix, Update, Remove)
   - Be concise but descriptive
   - Reference issues if applicable

5. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

### Before Submitting

Ensure your PR meets these requirements:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts with main branch

### Submitting a Pull Request

1. **Go to the original repository** on GitHub
2. **Click "New Pull Request"**
3. **Select your fork and branch**
4. **Fill out the PR template:**
   - Clear title describing the change
   - Detailed description of what and why
   - Reference related issues
   - List breaking changes (if any)

### PR Title Format

Use descriptive titles:
- `Add: User profile avatar upload feature`
- `Fix: Event registration email not sending`
- `Update: Improve event search performance`
- `Docs: Add storage configuration guide`

### Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be attributed in the commit history

### What to Expect

- Initial review within 3-5 business days
- Constructive feedback if changes are needed
- Merge after approval and passing all checks

## Testing Requirements

### Writing Tests

All new features and bug fixes must include tests.

1. **Test Location:**
   - Place tests in the `tests.py` file of the relevant app
   - Use descriptive test method names

2. **Test Coverage:**
   - Test happy paths (expected behavior)
   - Test edge cases
   - Test error handling
   - Test permissions and authentication

3. **Example Test:**
   ```python
   from django.test import TestCase
   from django.contrib.auth.models import User
   from events.models import Event
   
   
   class EventModelTest(TestCase):
       def setUp(self):
           self.user = User.objects.create_user(
               username='testuser',
               password='testpass123'
           )
           
       def test_create_event(self):
           """Test creating a new event"""
           event = Event.objects.create(
               title='Test Event',
               organizer=self.user,
               max_attendees=50
           )
           self.assertEqual(event.title, 'Test Event')
           self.assertEqual(event.organizer, self.user)
           
       def test_event_str_representation(self):
           """Test the string representation of Event"""
           event = Event.objects.create(
               title='Test Event',
               organizer=self.user
           )
           self.assertEqual(str(event), 'Test Event')
   ```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test events
python manage.py test users

# Run specific test case
python manage.py test events.tests.EventModelTest

# Run with verbose output
python manage.py test --verbosity=2

# Generate coverage report
coverage run manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

### Test Requirements for PRs

- All tests must pass
- New features must have test coverage
- Bug fixes should include regression tests
- Aim for high code coverage (>80% preferred)

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

1. **Clear title** describing the issue
2. **Steps to reproduce** the bug
3. **Expected behavior** vs actual behavior
4. **Environment details:**
   - OS and version
   - Python version
   - Django version
   - Browser (if UI-related)
5. **Error messages** or screenshots
6. **Relevant code snippets** (if applicable)

### Feature Requests

When requesting features, please include:

1. **Clear description** of the feature
2. **Use case:** Why is this feature needed?
3. **Proposed solution** (if you have ideas)
4. **Alternatives considered**
5. **Additional context** or examples

### Security Issues

**Do not** report security vulnerabilities in public issues. Instead:

1. Email the maintainers directly
2. Include details of the vulnerability
3. Wait for confirmation before public disclosure

## Contact

- **GitHub Issues:** For bug reports and feature requests
- **Pull Requests:** For code contributions
- **Discussions:** For questions and general discussion

## Additional Resources

- [Development Guide](DEVELOPMENT.md) - Detailed development setup
- [Deployment Guide](DEPLOYMENT.md) - Production deployment instructions
- [Documentation](docs/) - Full project documentation
- [Dependencies](DEPENDENCIES.md) - Third-party licenses and dependencies

## Thank You!

Thank you for contributing to Event Horizon! Your efforts help make this project better for everyone. We appreciate your time and expertise.

---

**Remember:** By contributing, you agree that your contributions will be licensed under the GPL-3.0 license.
