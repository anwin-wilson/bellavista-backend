#!/usr/bin/env python
"""
Local development setup script
"""
import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n{description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} completed")
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        return False
    return True

def main():
    print("🚀 Bellavista Backend Setup")
    print("=" * 30)
    
    if not os.path.exists('venv'):
        run_command('python -m venv venv', 'Creating virtual environment')
    
    run_command('venv\\Scripts\\pip install -r requirements.txt', 'Installing dependencies')
    run_command('venv\\Scripts\\python manage.py migrate', 'Running migrations')
    run_command('venv\\Scripts\\python manage.py collectstatic --noinput', 'Collecting static files')
    
    print("\n✅ Setup completed!")
    print("\nStart server: venv\\Scripts\\python manage.py runserver")
    print("\nAPI Endpoints:")
    print("- POST /api/tours/book/")
    print("- GET /api/tours/bookings/")
    print("- GET /api/tours/available-slots/")
    print("- GET /api/tours/stats/")
    print("- GET /api/tours/test/")

if __name__ == '__main__':
    main()