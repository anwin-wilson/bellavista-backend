#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellavista_backend.settings')
os.environ['SENDGRID_API_KEY'] = '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'

django.setup()

from tours.email_service import send_test_email

print("🧪 TESTING SENDGRID LOCALLY")
print("=" * 40)

# Test SendGrid
result = send_test_email('anwinws@gmail.com')

if result['success']:
    print("✅ SendGrid test successful!")
    print(f"📧 Email sent to anwinws@gmail.com")
else:
    print(f"❌ SendGrid failed: {result['error']}")

print("\nIf this works, deploy to Render and test live!")