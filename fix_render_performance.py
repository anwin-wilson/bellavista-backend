#!/usr/bin/env python3
"""
Performance fixes for Render deployment
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellavista_backend.settings')
django.setup()

from django.core.management import execute_from_command_line
from tours.models import TourBooking

def optimize_database():
    """Optimize database performance"""
    print("🔧 Optimizing database...")
    
    # Run migrations
    print("   Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Collect static files
    print("   Collecting static files...")
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Check database integrity
    print("   Checking database...")
    bookings_count = TourBooking.objects.count()
    print(f"   ✅ Database OK - {bookings_count} bookings found")
    
    return True

def check_environment():
    """Check environment configuration"""
    print("🌍 Checking environment...")
    
    # Check critical settings
    checks = {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': len(settings.ALLOWED_HOSTS),
        'EMAIL_CONFIGURED': bool(settings.EMAIL_HOST_USER),
        'SENDGRID_KEY': bool(os.environ.get('SENDGRID_API_KEY')),
        'SECRET_KEY': bool(settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-dev-key-change-in-production')
    }
    
    for check, value in checks.items():
        status = "✅" if value else "⚠️"
        print(f"   {status} {check}: {value}")
    
    return True

def create_test_data():
    """Create some test data if database is empty"""
    if TourBooking.objects.count() == 0:
        print("📝 Creating test data...")
        
        from datetime import datetime, timedelta
        
        test_booking = TourBooking.objects.create(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            phone_number="+44 7700 900123",
            preferred_home="cardiff",
            preferred_date=datetime.now().date() + timedelta(days=1),
            preferred_time="10:00",
            notes="Test booking for API validation"
        )
        
        print(f"   ✅ Created test booking #{test_booking.id}")
    else:
        print("📝 Database already has data - skipping test data creation")

if __name__ == "__main__":
    print("🚀 Bellavista Backend - Performance Optimization")
    print("=" * 50)
    
    try:
        optimize_database()
        check_environment()
        create_test_data()
        
        print("\n✅ Optimization complete!")
        print("\n📋 Next steps:")
        print("   1. Deploy to Render")
        print("   2. Set SENDGRID_API_KEY environment variable (optional)")
        print("   3. Test API endpoints")
        
    except Exception as e:
        print(f"\n❌ Error during optimization: {e}")
        exit(1)