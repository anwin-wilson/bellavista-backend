#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellavista_backend.settings')
    
    try:
        from django.core.management import execute_from_command_line
        
        # Run migrations first
        print("Running migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Start server
        print("Starting server at http://localhost:8000")
        print("API endpoints:")
        print("- POST /api/tours/book/ - Create booking")
        print("- GET /api/tours/bookings/ - List bookings")
        print("- GET /api/tours/available-slots/ - Available slots")
        print("- GET /api/tours/stats/ - Booking statistics")
        
        execute_from_command_line(['manage.py', 'runserver'])
        
    except ImportError as e:
        print(f"Error: {e}")
        print("Install dependencies: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == '__main__':
    main()