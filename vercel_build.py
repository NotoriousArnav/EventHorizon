#!/usr/bin/env python
"""
Vercel build hook for Django
Runs before the Python application is deployed
"""
import subprocess
import sys

def main():
    print("=" * 50)
    print("Running Vercel build process for Django")
    print("=" * 50)
    
    # Build CSS
    print("\n[1/2] Building Tailwind CSS...")
    subprocess.run(["npm", "run", "build:css"], check=True)
    
    # Collect static files
    print("\n[2/2] Collecting static files...")
    subprocess.run(["python", "manage.py", "collectstatic", "--noinput", "--clear"], check=True)
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        sys.exit(1)
