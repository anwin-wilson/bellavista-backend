#!/bin/bash
# Build script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Run Django setup commands
python manage.py migrate
python manage.py collectstatic --noinput