# WSGI Configuration for Bellavista Care Homes Backend
# This file is used by WSGI-compatible web servers to serve the Django project

import os
from django.core.wsgi import get_wsgi_application

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellavista_backend.settings')

# Create WSGI application
application = get_wsgi_application()