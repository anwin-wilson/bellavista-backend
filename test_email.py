#!/usr/bin/env python
"""
Email Test Script for Bellavista Care Homes
Run this script to test email functionality independently
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bellavista_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import time

def test_email_configuration():
    """Test email configuration and send a test email"""
    
    print("🔧 Testing Email Configuration...")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {settings.EMAIL_HOST}")
    print(f"Email Port: {settings.EMAIL_PORT}")
    print(f"Email User: {settings.EMAIL_HOST_USER}")
    print(f"Use TLS: {settings.EMAIL_USE_TLS}")
    print(f"Default From: {settings.DEFAULT_FROM_EMAIL}")
    print("-" * 50)
    
    if not settings.EMAIL_HOST_USER:
        print("❌ No email credentials configured!")
        print("Please set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env file")
        return False
    
    # Get test email from user
    test_email = input("Enter test email address: ").strip()
    if not test_email:
        print("❌ No email address provided!")
        return False
    
    try:
        print(f"📧 Sending test email to {test_email}...")
        start_time = time.time()
        
        send_mail(
            subject='Bellavista Care Homes - Email Test',
            message='''
Hello!

This is a test email from Bellavista Care Homes backend API.

If you received this email, the email configuration is working correctly!

Best regards,
Bellavista Care Homes Team
            '''.strip(),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        
        elapsed_time = time.time() - start_time
        print(f"✅ Email sent successfully in {elapsed_time:.2f} seconds!")
        return True
        
    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        print("\nCommon issues:")
        print("1. Check Gmail App Password (not regular password)")
        print("2. Ensure 2FA is enabled on Gmail account")
        print("3. Check firewall/network restrictions")
        print("4. Verify EMAIL_HOST_PASSWORD in .env file")
        return False

def test_booking_email():
    """Test booking confirmation email"""
    from tours.models import TourBooking
    from datetime import date, time as dt_time
    
    print("\n🎯 Testing Booking Confirmation Email...")
    
    # Create a test booking
    test_booking = TourBooking(
        first_name="Test",
        last_name="User",
        email=input("Enter email for booking test: ").strip(),
        phone_number="07123456789",
        preferred_home="cardiff",
        preferred_date=date.today(),
        preferred_time=dt_time(14, 0),
        notes="This is a test booking",
        status="pending"
    )
    
    try:
        from tours.views import TourBookingCreateView
        view = TourBookingCreateView()
        
        start_time = time.time()
        success = view.send_confirmation_email(test_booking)
        elapsed_time = time.time() - start_time
        
        if success:
            print(f"✅ Booking email sent successfully in {elapsed_time:.2f} seconds!")
        else:
            print("❌ Booking email failed!")
            
    except Exception as e:
        print(f"❌ Booking email test failed: {str(e)}")

if __name__ == "__main__":
    print("🚀 Bellavista Care Homes - Email Test")
    print("=" * 50)
    
    # Test basic email configuration
    if test_email_configuration():
        # Test booking-specific email
        test_booking_email()
    
    print("\n✨ Email testing completed!")