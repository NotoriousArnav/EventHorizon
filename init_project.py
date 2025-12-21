#!/usr/bin/env python3
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
Event Horizon - Initialization Protocol
Interactive setup script for configuring the Event Horizon platform.
Supports --no-interactive mode for automated setups using environment variables.
"""

import os
import subprocess
import sys
import secrets
import shutil
import argparse


def print_step(message):
    print(f"\n\033[1;36m[+] {message}\033[0m")


def print_success(message):
    print(f"\033[1;32m[✓] {message}\033[0m")


def print_error(message):
    print(f"\033[1;31m[!] {message}\033[0m")


def print_warning(message):
    print(f"\033[1;33m[!] {message}\033[0m")


def print_info(message):
    print(f"\033[0;36m    {message}\033[0m")


def run_command(command, description, suppress_errors=False):
    """Execute a shell command and return success status."""
    print_step(f"Executing: {description}...")
    try:
        if suppress_errors:
            subprocess.check_call(
                command,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.check_call(command, shell=True)
        print_success(f"{description} completed.")
        return True
    except subprocess.CalledProcessError:
        print_error(f"Failed to execute: {description}")
        return False


def check_command_exists(command):
    """Check if a command exists on the system."""
    return shutil.which(command) is not None


def run_build_script():
    """Execute the build.sh script if it exists."""
    if not os.path.exists("build.sh"):
        print_warning("build.sh not found, skipping build step.")
        return True

    print_step("Running build.sh script...")
    try:
        # Make the script executable
        os.chmod("build.sh", 0o755)
        subprocess.check_call("./build.sh", shell=True)
        print_success("build.sh executed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"build.sh execution failed: {e}")
        return False


def get_input(prompt, default="", validator=None, non_interactive=False, env_var=None):
    """Get user input with optional default and validation.

    Args:
        prompt: The prompt to display
        default: Default value if no input provided
        validator: Optional validation function
        non_interactive: If True, use default without prompting
        env_var: Environment variable name to check in non-interactive mode
    """
    # In non-interactive mode, get from env var or use default
    if non_interactive:
        if env_var and os.getenv(env_var):
            return os.getenv(env_var) or default
        return default

    while True:
        if default:
            response = input(f"{prompt} [{default}]: ").strip() or default
        else:
            response = input(f"{prompt}: ").strip()

        if validator:
            valid, message = validator(response)
            if not valid:
                print_error(message)
                continue

        return response


def yes_no(prompt, default=True, non_interactive=False, env_var=None):
    """Ask a yes/no question.

    Args:
        prompt: The prompt to display
        default: Default value (True or False)
        non_interactive: If True, use default without prompting
        env_var: Environment variable name to check in non-interactive mode
    """
    if non_interactive:
        if env_var and os.getenv(env_var):
            val = os.getenv(env_var, "").lower()
            return val in ["true", "yes", "1", "y"]
        return default

    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} ({default_str}): ").strip().lower()

    if not response:
        return default

    return response in ["y", "yes"]


def setup_dependencies():
    """Install project dependencies."""
    print_step("Checking dependencies protocol...")

    # Check if we are in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv and not os.path.exists(".venv"):
        print_warning("You are not in a virtual environment.")
        print_info("It's recommended to use a virtual environment.")

    # Check for uv
    has_uv = check_command_exists("uv")

    if has_uv and os.path.exists("uv.lock"):
        if yes_no("uv.lock detected. Use 'uv' to sync dependencies?", True):
            if run_command("uv sync", "Syncing dependencies with uv"):
                return True
            else:
                print_error("Make sure 'uv' is installed correctly.")
                return False
    elif has_uv:
        if yes_no("Use 'uv' to install dependencies?", True):
            if run_command("uv sync", "Syncing dependencies with uv"):
                return True

    # Fallback to pip
    if yes_no("Install dependencies using pip (from pyproject.toml)?", False):
        return run_command(
            f"{sys.executable} -m pip install -e .", "Installing dependencies via pip"
        )

    print_warning("Skipping dependency installation.")
    return True


def setup_env_file(non_interactive=False):
    """Create and configure .env file.

    Args:
        non_interactive: If True, use environment variables and defaults
    """
    print_step("Configuring environmental parameters (.env)...")

    if os.path.exists(".env"):
        if non_interactive:
            overwrite = os.getenv("OVERWRITE_ENV", "false").lower() in [
                "true",
                "yes",
                "1",
            ]
        else:
            overwrite = yes_no(".env file already exists. Overwrite?", False)

        if not overwrite:
            print_success("Keeping existing .env file.")
            return

    print_info("Creating .env configuration file...")

    env_config = {}

    # Django Core Settings
    if not non_interactive:
        print_info("\n--- Core Settings ---")
    env_config["SECRET_KEY"] = os.getenv("SECRET_KEY", secrets.token_urlsafe(50))
    print_success(f"Generated secure SECRET_KEY")

    if non_interactive:
        env_config["DEBUG"] = os.getenv("DEBUG", "True")
    else:
        env_config["DEBUG"] = "True" if yes_no("Enable DEBUG mode?", True) else "False"

    env_config["ALLOWED_HOSTS"] = os.getenv(
        "ALLOWED_HOSTS", "127.0.0.1,localhost,0.0.0.0"
    )

    # Database Configuration
    if not non_interactive:
        print_info("\n--- Database Configuration ---")
        print_info("1. SQLite (default, simple)")
        print_info("2. PostgreSQL (production recommended)")
        print_info("3. MySQL/MariaDB")
        print_info("4. Custom DATABASE_URL")

    db_choice = get_input(
        "Select database", "1", non_interactive=non_interactive, env_var="DB_TYPE"
    )

    if db_choice == "1":
        print_success("Using SQLite (default)")
        # No DATABASE_URL needed
    elif db_choice == "2":
        if not non_interactive:
            print_info("PostgreSQL configuration:")
            print_warning("Make sure to install: uv add psycopg2-binary")
        db_user = get_input(
            "Database user",
            "postgres",
            non_interactive=non_interactive,
            env_var="DB_USER",
        )
        db_pass = get_input(
            "Database password",
            "postgres",
            non_interactive=non_interactive,
            env_var="DB_PASSWORD",
        )
        db_host = get_input(
            "Database host",
            "localhost",
            non_interactive=non_interactive,
            env_var="DB_HOST",
        )
        db_port = get_input(
            "Database port", "5432", non_interactive=non_interactive, env_var="DB_PORT"
        )
        db_name = get_input(
            "Database name",
            "eventhorizon",
            non_interactive=non_interactive,
            env_var="DB_NAME",
        )
        env_config["DATABASE_URL"] = (
            f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        print_success("PostgreSQL configuration added")
    elif db_choice == "3":
        if not non_interactive:
            print_info("MySQL/MariaDB configuration:")
            print_warning("Make sure to install: uv add mysqlclient")
        db_user = get_input(
            "Database user", "root", non_interactive=non_interactive, env_var="DB_USER"
        )
        db_pass = get_input(
            "Database password",
            "",
            non_interactive=non_interactive,
            env_var="DB_PASSWORD",
        )
        db_host = get_input(
            "Database host",
            "localhost",
            non_interactive=non_interactive,
            env_var="DB_HOST",
        )
        db_port = get_input(
            "Database port", "3306", non_interactive=non_interactive, env_var="DB_PORT"
        )
        db_name = get_input(
            "Database name",
            "eventhorizon",
            non_interactive=non_interactive,
            env_var="DB_NAME",
        )
        env_config["DATABASE_URL"] = (
            f"mysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        print_success("MySQL configuration added")
    elif db_choice == "4":
        db_url = get_input(
            "Enter DATABASE_URL",
            "",
            non_interactive=non_interactive,
            env_var="DATABASE_URL",
        )
        if db_url:
            env_config["DATABASE_URL"] = db_url
            print_success("Custom DATABASE_URL added")

    # CORS Configuration
    if not non_interactive:
        print_info("\n--- CORS Configuration ---")

    if yes_no(
        "Allow all origins (developer-friendly, APIs are OAuth2-protected)?",
        True,
        non_interactive=non_interactive,
        env_var="CORS_ALLOW_ALL",
    ):
        env_config["CORS_ALLOW_ALL_ORIGINS"] = "True"
    else:
        origins = get_input(
            "Enter allowed origins (comma-separated)",
            "http://localhost:3000",
            non_interactive=non_interactive,
            env_var="CORS_ORIGINS",
        )
        env_config["CORS_ALLOW_ALL_ORIGINS"] = "False"
        env_config["CORS_ALLOWED_ORIGINS"] = origins

    # Email Configuration
    if not non_interactive:
        print_info("\n--- Email Configuration ---")
        print_info("1. Console (development - prints to terminal)")
        print_info("2. SMTP (Gmail, AWS SES, etc.)")
        print_info("3. SendGrid")
        print_info("4. Mailgun")

    email_choice = get_input(
        "Select email backend",
        "1",
        non_interactive=non_interactive,
        env_var="EMAIL_BACKEND_TYPE",
    )

    if email_choice == "1":
        env_config["EMAIL_BACKEND"] = "console"
        print_success("Using console email backend")
    elif email_choice == "2":
        env_config["EMAIL_BACKEND"] = "smtp"
        env_config["EMAIL_HOST"] = get_input(
            "SMTP host",
            "smtp.gmail.com",
            non_interactive=non_interactive,
            env_var="EMAIL_HOST",
        )
        env_config["EMAIL_PORT"] = get_input(
            "SMTP port", "587", non_interactive=non_interactive, env_var="EMAIL_PORT"
        )
        env_config["EMAIL_USE_TLS"] = "True"
        env_config["EMAIL_HOST_USER"] = get_input(
            "Email address",
            "",
            non_interactive=non_interactive,
            env_var="EMAIL_HOST_USER",
        )
        env_config["EMAIL_HOST_PASSWORD"] = get_input(
            "Email password/app password",
            "",
            non_interactive=non_interactive,
            env_var="EMAIL_HOST_PASSWORD",
        )
        env_config["DEFAULT_FROM_EMAIL"] = get_input(
            "From email",
            env_config.get("EMAIL_HOST_USER", ""),
            non_interactive=non_interactive,
            env_var="DEFAULT_FROM_EMAIL",
        )
        print_success("SMTP configuration added")
        if not non_interactive and "gmail.com" in env_config.get("EMAIL_HOST", ""):
            print_info(
                "Note: For Gmail, use an App Password (not your regular password)"
            )
            print_info("Generate one at: https://myaccount.google.com/apppasswords")
    elif email_choice == "3":
        env_config["EMAIL_BACKEND"] = "sendgrid"
        env_config["SENDGRID_API_KEY"] = get_input(
            "SendGrid API key",
            "",
            non_interactive=non_interactive,
            env_var="SENDGRID_API_KEY",
        )
        env_config["DEFAULT_FROM_EMAIL"] = get_input(
            "From email",
            "noreply@yourdomain.com",
            non_interactive=non_interactive,
            env_var="DEFAULT_FROM_EMAIL",
        )
        if not non_interactive:
            print_warning("Make sure to install: pip install sendgrid-django")
        print_success("SendGrid configuration added")
    elif email_choice == "4":
        env_config["EMAIL_BACKEND"] = "mailgun"
        env_config["MAILGUN_API_KEY"] = get_input(
            "Mailgun API key",
            "",
            non_interactive=non_interactive,
            env_var="MAILGUN_API_KEY",
        )
        env_config["MAILGUN_SENDER_DOMAIN"] = get_input(
            "Mailgun sender domain",
            "",
            non_interactive=non_interactive,
            env_var="MAILGUN_SENDER_DOMAIN",
        )
        env_config["DEFAULT_FROM_EMAIL"] = get_input(
            "From email",
            "noreply@yourdomain.com",
            non_interactive=non_interactive,
            env_var="DEFAULT_FROM_EMAIL",
        )
        if not non_interactive:
            print_warning("Make sure to install: pip install django-anymail")
        print_success("Mailgun configuration added")

    # Storage Configuration
    if not non_interactive:
        print_info("\n--- Storage Configuration ---")
        print_info("1. Local filesystem (development)")
        print_info("2. AWS S3")
        print_info("3. MinIO (self-hosted S3-compatible)")
        print_info("4. DigitalOcean Spaces")
        print_info("5. Cloudflare R2")

    storage_choice = get_input(
        "Select storage backend",
        "1",
        non_interactive=non_interactive,
        env_var="STORAGE_TYPE",
    )

    if storage_choice == "1":
        env_config["STORAGE_BACKEND"] = "local"
        print_success("Using local filesystem storage")
    elif storage_choice == "2":
        env_config["STORAGE_BACKEND"] = "s3"
        env_config["AWS_ACCESS_KEY_ID"] = get_input(
            "AWS Access Key ID",
            "",
            non_interactive=non_interactive,
            env_var="AWS_ACCESS_KEY_ID",
        )
        env_config["AWS_SECRET_ACCESS_KEY"] = get_input(
            "AWS Secret Access Key",
            "",
            non_interactive=non_interactive,
            env_var="AWS_SECRET_ACCESS_KEY",
        )
        env_config["AWS_STORAGE_BUCKET_NAME"] = get_input(
            "S3 Bucket name",
            "",
            non_interactive=non_interactive,
            env_var="AWS_STORAGE_BUCKET_NAME",
        )
        env_config["AWS_S3_REGION_NAME"] = get_input(
            "AWS Region",
            "us-east-1",
            non_interactive=non_interactive,
            env_var="AWS_S3_REGION_NAME",
        )
        env_config["AWS_S3_USE_SSL"] = "True"
        print_success("AWS S3 configuration added")
    elif storage_choice == "3":
        env_config["STORAGE_BACKEND"] = "minio"
        env_config["AWS_ACCESS_KEY_ID"] = get_input(
            "MinIO Access Key",
            "minioadmin",
            non_interactive=non_interactive,
            env_var="AWS_ACCESS_KEY_ID",
        )
        env_config["AWS_SECRET_ACCESS_KEY"] = get_input(
            "MinIO Secret Key",
            "minioadmin",
            non_interactive=non_interactive,
            env_var="AWS_SECRET_ACCESS_KEY",
        )
        env_config["AWS_STORAGE_BUCKET_NAME"] = get_input(
            "Bucket name",
            "eventhorizon",
            non_interactive=non_interactive,
            env_var="AWS_STORAGE_BUCKET_NAME",
        )
        env_config["AWS_S3_ENDPOINT_URL"] = get_input(
            "MinIO endpoint",
            "http://localhost:9000",
            non_interactive=non_interactive,
            env_var="AWS_S3_ENDPOINT_URL",
        )
        env_config["AWS_S3_USE_SSL"] = "False"
        env_config["AWS_S3_REGION_NAME"] = "us-east-1"
        print_success("MinIO configuration added")
    elif storage_choice == "4":
        env_config["STORAGE_BACKEND"] = "s3"
        env_config["AWS_ACCESS_KEY_ID"] = get_input(
            "Spaces Access Key",
            "",
            non_interactive=non_interactive,
            env_var="AWS_ACCESS_KEY_ID",
        )
        env_config["AWS_SECRET_ACCESS_KEY"] = get_input(
            "Spaces Secret Key",
            "",
            non_interactive=non_interactive,
            env_var="AWS_SECRET_ACCESS_KEY",
        )
        env_config["AWS_STORAGE_BUCKET_NAME"] = get_input(
            "Space name",
            "",
            non_interactive=non_interactive,
            env_var="AWS_STORAGE_BUCKET_NAME",
        )
        region = get_input(
            "Region (e.g., nyc3, sfo2)",
            "nyc3",
            non_interactive=non_interactive,
            env_var="AWS_S3_REGION",
        )
        env_config["AWS_S3_ENDPOINT_URL"] = f"https://{region}.digitaloceanspaces.com"
        env_config["AWS_S3_REGION_NAME"] = "us-east-1"
        env_config["AWS_S3_USE_SSL"] = "True"
        print_success("DigitalOcean Spaces configuration added")
    elif storage_choice == "5":
        env_config["STORAGE_BACKEND"] = "s3"
        env_config["AWS_ACCESS_KEY_ID"] = get_input(
            "R2 Access Key ID",
            "",
            non_interactive=non_interactive,
            env_var="AWS_ACCESS_KEY_ID",
        )
        env_config["AWS_SECRET_ACCESS_KEY"] = get_input(
            "R2 Secret Access Key",
            "",
            non_interactive=non_interactive,
            env_var="AWS_SECRET_ACCESS_KEY",
        )
        env_config["AWS_STORAGE_BUCKET_NAME"] = get_input(
            "R2 Bucket name",
            "",
            non_interactive=non_interactive,
            env_var="AWS_STORAGE_BUCKET_NAME",
        )
        account_id = get_input(
            "Cloudflare Account ID",
            "",
            non_interactive=non_interactive,
            env_var="CLOUDFLARE_ACCOUNT_ID",
        )
        env_config["AWS_S3_ENDPOINT_URL"] = (
            f"https://{account_id}.r2.cloudflarestorage.com"
        )
        env_config["AWS_S3_REGION_NAME"] = "auto"
        env_config["AWS_S3_USE_SSL"] = "True"
        print_success("Cloudflare R2 configuration added")

    # Write .env file
    with open(".env", "w") as f:
        f.write("# Event Horizon Configuration\n")
        f.write("# Generated by init_project.py\n\n")

        f.write("# Django Core Settings\n")
        f.write(f"SECRET_KEY={env_config['SECRET_KEY']}\n")
        f.write(f"DEBUG={env_config['DEBUG']}\n")
        f.write(f"ALLOWED_HOSTS={env_config['ALLOWED_HOSTS']}\n\n")

        if "DATABASE_URL" in env_config:
            f.write("# Database Configuration\n")
            f.write(f"DATABASE_URL={env_config['DATABASE_URL']}\n\n")

        f.write("# CORS Settings\n")
        f.write(f"CORS_ALLOW_ALL_ORIGINS={env_config['CORS_ALLOW_ALL_ORIGINS']}\n")
        if "CORS_ALLOWED_ORIGINS" in env_config:
            f.write(f"CORS_ALLOWED_ORIGINS={env_config['CORS_ALLOWED_ORIGINS']}\n")
        f.write("\n")

        f.write("# Email Configuration\n")
        f.write(f"EMAIL_BACKEND={env_config['EMAIL_BACKEND']}\n")
        for key in [
            "EMAIL_HOST",
            "EMAIL_PORT",
            "EMAIL_USE_TLS",
            "EMAIL_HOST_USER",
            "EMAIL_HOST_PASSWORD",
            "DEFAULT_FROM_EMAIL",
            "SENDGRID_API_KEY",
            "MAILGUN_API_KEY",
            "MAILGUN_SENDER_DOMAIN",
        ]:
            if key in env_config:
                f.write(f"{key}={env_config[key]}\n")
        f.write("\n")

        f.write("# Storage Configuration\n")
        f.write(f"STORAGE_BACKEND={env_config['STORAGE_BACKEND']}\n")
        for key in [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_S3_REGION_NAME",
            "AWS_S3_ENDPOINT_URL",
            "AWS_S3_USE_SSL",
        ]:
            if key in env_config:
                f.write(f"{key}={env_config[key]}\n")
        f.write("\n")

        f.write("# OAuth2/OIDC Settings\n")
        f.write("OIDC_RSA_PRIVATE_KEY=\n")

    print_success("Generated .env file with configuration.")


def setup_frontend():
    """Setup Node.js dependencies and Tailwind CSS."""
    print_step("Setting up frontend build system...")

    if not os.path.exists("package.json"):
        print_success("No package.json found. Skipping Node.js setup.")
        return

    # Check for Node.js
    if not check_command_exists("node"):
        print_error("Node.js is not installed!")
        print_info("Download from: https://nodejs.org/")
        return

    if not check_command_exists("npm"):
        print_error("npm is not installed!")
        return

    print_success("Node.js and npm detected.")

    if yes_no("Install Node.js dependencies (npm install)?", True):
        if run_command("npm install", "Installing Node.js dependencies"):
            # Build Tailwind CSS
            if yes_no("Build Tailwind CSS now?", True):
                if run_command("npm run build:css", "Building Tailwind CSS"):
                    print_success("Tailwind CSS compiled successfully.")
                    print_info(
                        "Tip: Run 'npm run watch:css' during development for auto-rebuild."
                    )
        else:
            print_error("Failed to install Node.js dependencies.")


def setup_database():
    """Run database migrations."""
    print_step("Initializing database systems...")

    python_cmd = sys.executable

    # Check Django installation
    if not run_command(
        f"{python_cmd} -c 'import django; print(django.get_version())'",
        "Verifying Django installation",
        suppress_errors=True,
    ):
        print_error("Django is not installed or not accessible.")
        print_info("Make sure you've installed dependencies.")
        return False

    # Run migrations
    if not run_command(
        f"{python_cmd} manage.py migrate", "Applying database migrations"
    ):
        print_error("Database migration failed!")
        print_info("Check your database configuration in .env")
        return False

    return True


def setup_superuser(non_interactive=False):
    """Create superuser account.

    Args:
        non_interactive: If True, use environment variables and defaults
    """
    print_step("User Access Control...")

    python_cmd = sys.executable

    # Check if user wants to create a superuser
    create = True
    if non_interactive:
        create = os.getenv("CREATE_SUPERUSER", "true").lower() in ["true", "yes", "1"]
    else:
        create = yes_no("Create a superuser account now?", True)

    if not create:
        print_info(
            "You can create a superuser later with: python manage.py createsuperuser"
        )
        return

    # Import the create_superuser function
    try:
        # Add current directory to path to import create_superuser module
        sys.path.insert(0, os.getcwd())
        from create_superuser import setup_django, create_superuser as create_su_func

        # Setup Django
        setup_django()

        # Get credentials from environment or use defaults
        username = os.getenv("SUPERUSER_USERNAME", "admin")
        email = os.getenv("SUPERUSER_EMAIL", "admin@eventhorizon.local")
        password = os.getenv("SUPERUSER_PASSWORD", "Ihapwics123$")
        first_name = os.getenv("SUPERUSER_FIRST_NAME", "Administrator")
        last_name = os.getenv("SUPERUSER_LAST_NAME", "Staff")

        # Create the superuser
        success, message = create_su_func(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            verbose=not non_interactive,
        )

        if success and not non_interactive:
            print_success(f"Superuser created: {username} / {password}")

    except ImportError as e:
        print_warning(f"Could not import create_superuser module: {e}")
        print_info("Falling back to interactive creation...")
        if not non_interactive:
            run_command(
                f"{python_cmd} manage.py createsuperuser",
                "Interactive superuser creation",
            )
    except Exception as e:
        print_error(f"Failed to create superuser: {e}")
        if not non_interactive and yes_no("Try interactive creation?", True):
            run_command(
                f"{python_cmd} manage.py createsuperuser",
                "Interactive superuser creation",
            )


def print_next_steps():
    """Print final instructions."""
    python_cmd = sys.executable

    print("\n\033[1;35m" + "=" * 60)
    print("      SYSTEM INITIALIZATION COMPLETE")
    print("=" * 60 + "\033[0m")

    print("\n\033[1;32mNext Steps:\033[0m")
    print("\n1. Start the development server:")
    print(f"   \033[1;36m{python_cmd} manage.py runserver\033[0m")

    print("\n2. For Tailwind CSS development (auto-rebuild on changes):")
    print("   \033[1;36mnpm run watch:css\033[0m")

    print("\n3. Access the platform:")
    print("   \033[1;36mhttp://127.0.0.1:8000\033[0m")

    print("\n4. Admin panel:")
    print("   \033[1;36mhttp://127.0.0.1:8000/admin\033[0m")

    print("\n\033[1;33mUseful Commands:\033[0m")
    print(f"   Create migrations:  {python_cmd} manage.py makemigrations")
    print(f"   Apply migrations:   {python_cmd} manage.py migrate")
    print(f"   Create superuser:   {python_cmd} manage.py createsuperuser")
    print(f"   Collect static:     {python_cmd} manage.py collectstatic")
    print(f"   Run tests:          {python_cmd} manage.py test")

    print("\n\033[1;36mDocumentation:\033[0m")
    print("   Setup Guide:        docs/setup/installation.md")
    print("   Configuration:      docs/setup/configuration.md")
    print("   Development:        DEVELOPMENT.md")
    print("   Deployment:         DEPLOYMENT.md")

    print("\n\033[1;32m✓ Ready to launch Event Horizon!\033[0m\n")


def main():
    """Main initialization workflow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Event Horizon Initialization Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment Variables (used in --no-interactive mode):
  OVERWRITE_ENV           - Overwrite existing .env (true/false)
  SECRET_KEY              - Django secret key
  DEBUG                   - Enable debug mode (true/false)
  ALLOWED_HOSTS           - Comma-separated allowed hosts
  DB_TYPE                 - Database type (1=SQLite, 2=PostgreSQL, 3=MySQL, 4=Custom)
  DB_USER                 - Database username
  DB_PASSWORD             - Database password
  DB_HOST                 - Database host
  DB_PORT                 - Database port
  DB_NAME                 - Database name
  DATABASE_URL            - Full database URL (for custom DB)
  CORS_ALLOW_ALL          - Allow all CORS origins (true/false)
  CORS_ORIGINS            - Comma-separated CORS origins
  EMAIL_BACKEND_TYPE      - Email backend (1=Console, 2=SMTP, 3=SendGrid, 4=Mailgun)
  EMAIL_HOST              - SMTP host
  EMAIL_PORT              - SMTP port
  EMAIL_HOST_USER         - Email username
  EMAIL_HOST_PASSWORD     - Email password
  DEFAULT_FROM_EMAIL      - Default from email
  SENDGRID_API_KEY        - SendGrid API key
  MAILGUN_API_KEY         - Mailgun API key
  MAILGUN_SENDER_DOMAIN   - Mailgun sender domain
  STORAGE_TYPE            - Storage backend (1=Local, 2=S3, 3=MinIO, 4=DO Spaces, 5=R2)
  AWS_ACCESS_KEY_ID       - AWS/S3 access key
  AWS_SECRET_ACCESS_KEY   - AWS/S3 secret key
  AWS_STORAGE_BUCKET_NAME - S3 bucket name
  AWS_S3_REGION_NAME      - S3 region
  AWS_S3_ENDPOINT_URL     - S3 endpoint URL (for MinIO/R2/Spaces)
  CLOUDFLARE_ACCOUNT_ID   - Cloudflare R2 account ID
  CREATE_SUPERUSER        - Create superuser (true/false)
  SUPERUSER_USERNAME      - Superuser username
  SUPERUSER_EMAIL         - Superuser email
  SUPERUSER_PASSWORD      - Superuser password
  SUPERUSER_FIRST_NAME    - Superuser first name
  SUPERUSER_LAST_NAME     - Superuser last name
  RUN_BUILD_SH            - Run build.sh script (true/false, default: false)
        """,
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Run in non-interactive mode using environment variables and defaults",
    )
    parser.add_argument(
        "--skip-build", action="store_true", help="Skip running build.sh script"
    )

    args = parser.parse_args()
    non_interactive = args.no_interactive

    if non_interactive:
        print("\033[1;35m" + "=" * 60)
        print("      EVENT HORIZON - NON-INTERACTIVE SETUP")
        print("=" * 60 + "\033[0m")
        print_info("Using environment variables and defaults for configuration.\n")
    else:
        print("\033[1;35m" + "=" * 60)
        print("      EVENT HORIZON - INITIALIZATION PROTOCOL")
        print("=" * 60 + "\033[0m")

        print_info("This script will guide you through the setup process.")
        print_info("Press Ctrl+C at any time to cancel.\n")

    try:
        # Step 0: Run build.sh if requested (only in non-interactive or explicit request)
        should_run_build = False
        if non_interactive:
            should_run_build = os.getenv("RUN_BUILD_SH", "false").lower() in [
                "true",
                "yes",
                "1",
            ]

        if should_run_build and not args.skip_build:
            if not run_build_script():
                print_warning("build.sh failed, but continuing with setup...")

        # Step 1: Dependencies (skip if build.sh was run)
        if not should_run_build:
            if not setup_dependencies():
                print_error("Dependency installation failed. Continuing anyway...")

        # Step 2: Environment Configuration
        setup_env_file(non_interactive=non_interactive)

        # Step 3: Frontend Build System (skip if build.sh was run)
        if not should_run_build:
            setup_frontend()

        # Step 4: Database Setup
        if setup_database():
            # Step 5: Superuser Creation
            setup_superuser(non_interactive=non_interactive)
        else:
            print_warning("Skipping superuser creation due to database setup failure.")

        # Final Instructions
        if not non_interactive:
            print_next_steps()
        else:
            print_success("\nSetup completed successfully!")

    except KeyboardInterrupt:
        print("\n\n\033[1;31m[!] Initialization cancelled by user.\033[0m")
        sys.exit(1)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
