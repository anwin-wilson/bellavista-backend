#!/usr/bin/env python
# Django Management Script for Bellavista Care Homes Backend
# This is the main entry point for running Django commands

import os
import sys


def main():
    """
    Main function to run Django administrative tasks.
    
    Common commands:
    - python manage.py runserver (start development server)
    - python manage.py migrate (apply database changes)
    - python manage.py createsuperuser (create admin user)
    - python manage.py collectstatic (collect static files)
    """
    # Set the default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellavista_backend.settings')
    
    try:
        # Import Django's command-line utility
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Provide helpful error message if Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command-line arguments
    execute_from_command_line(sys.argv)


# Run main function when script is executed directly
if __name__ == '__main__':
    main()