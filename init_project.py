import os
import subprocess
import sys
import secrets
import time


def print_step(message):
    print(f"\n\033[1;36m[+] {message}\033[0m")


def print_success(message):
    print(f"\033[1;32m[✓] {message}\033[0m")


def print_error(message):
    print(f"\033[1;31m[!] {message}\033[0m")


def run_command(command, description):
    print_step(f"Executing: {description}...")
    try:
        subprocess.check_call(command, shell=True)
        print_success(f"{description} completed.")
        return True
    except subprocess.CalledProcessError:
        print_error(f"Failed to execute: {description}")
        return False


def main():
    print("\033[1;35m" + "=" * 50)
    print("      EVENT HORIZON - INITIALIZATION PROTOCOL")
    print("=" * 50 + "\033[0m")

    # 1. Dependency Installation
    print_step("Checking dependencies protocol...")
    # Check if we are in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv and not os.path.exists(".venv") and not os.path.exists("uv.lock"):
        print("\033[1;33mWarning: You are not in a virtual environment.\033[0m")

    if os.path.exists("uv.lock"):
        choice = (
            input("uv.lock detected. Use 'uv' to sync dependencies? (Y/n): ")
            .strip()
            .lower()
        )
        if choice != "n":
            if not run_command("uv sync", "Syncing dependencies with uv"):
                print_error(
                    "Make sure 'uv' is installed. You can install it via 'pip install uv'."
                )
    else:
        choice = (
            input("Install dependencies using pip (from pyproject.toml)? (y/N): ")
            .strip()
            .lower()
        )
        if choice == "y":
            run_command(
                f"{sys.executable} -m pip install .", "Installing dependencies via pip"
            )

    # 2. Environment Setup
    print_step("Configuring environmental parameters (.env)...")
    if not os.path.exists(".env"):
        print("No .env file found. Creating one.")
        secret_key = secrets.token_urlsafe(50)
        debug_mode = input("Enable DEBUG mode? (Y/n): ").strip().lower() != "n"

        env_content = f"SECRET_KEY={secret_key}\nDEBUG={str(debug_mode)}\n"

        email_console = (
            input("Use Console Email Backend (prints emails to terminal)? (Y/n): ")
            .strip()
            .lower()
            != "n"
        )
        env_content += f"EMAIL2CONSOLE={str(email_console)}\n"

        with open(".env", "w") as f:
            f.write(env_content)
        print_success("Generated .env file with secure keys.")
    else:
        print_success(".env file already exists. Skipping.")

    # 3. Database Migration
    print_step("Initializing database systems...")
    # Use the python executable from the current environment (which might be the venv uv just created)
    # If uv created a venv, it's usually in .venv. We should try to use that python if it exists and we aren't currently using it.
    python_cmd = sys.executable

    # Simple check: if uv sync was run, it likely created .venv.
    # If we are not currently running from .venv, we might want to warn the user or try to use it.
    # For simplicity in this script, we assume the user will activate the shell or the dependencies are installed where this script runs.

    if run_command(f"{python_cmd} manage.py migrate", "Applying database migrations"):
        # 4. Superuser Creation
        print_step("User Access Control...")
        create_su = input("Create a superuser account now? (Y/n): ").strip().lower()
        if create_su != "n":
            # Check for helper script
            if os.path.exists("create_superuser.py"):
                use_script = (
                    input("Use automated script (creates user 'admin')? (Y/n): ")
                    .strip()
                    .lower()
                )
                if use_script != "n":
                    run_command(
                        f"{python_cmd} create_superuser.py",
                        "Running automated superuser creation script",
                    )
                else:
                    run_command(
                        f"{python_cmd} manage.py createsuperuser",
                        "Interactive superuser creation",
                    )
            else:
                run_command(
                    f"{python_cmd} manage.py createsuperuser",
                    "Interactive superuser creation",
                )

    print("\n\033[1;35m" + "=" * 50)
    print("      SYSTEM INITIALIZATION COMPLETE")
    print("=" * 50 + "\033[0m")
    print("\nTo launch the platform, run:")
    print(f"    {python_cmd} manage.py runserver")


if __name__ == "__main__":
    main()
