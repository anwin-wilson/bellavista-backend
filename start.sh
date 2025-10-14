#!/bin/bash
# Start script for Render deployment

# Start the Django application with Gunicorn
gunicorn bellavista_backend.wsgi:application --bind 0.0.0.0:$PORT