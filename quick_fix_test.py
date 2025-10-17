#!/usr/bin/env python3
"""
Quick test to verify the booking creation fix
"""

import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta

BASE_URL = "https://bellavista-backend-production.up.railway.app"

def test_booking_creation():
    """Test booking creation with timeout fix"""
    print("🚀 Testing Booking Creation Fix")
    print("=" * 40)
    
    # Test data
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    booking_data = {
        "first_name": "Quick",
        "last_name": "Test",
        "email": "quicktest@example.com",
        "phone_number": "+44 7700 900999",
        "preferred_home": "cardiff",
        "preferred_date": tomorrow,
        "preferred_time": "15:00",
        "notes": "Quick timeout fix test"
    }
    
    url = f"{BASE_URL}/api/tours/book/"
    json_data = json.dumps(booking_data).encode('utf-8')
    
    try:
        req = urllib.request.Request(url, data=json_data)
        req.add_header('Content-Type', 'application/json')
        
        print("📝 Creating booking...")
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            data = json.loads(content)
            
            print(f"✅ Status: {response.getcode()}")
            print(f"📋 Response: {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                print(f"🎯 Booking ID: {data.get('booking_id')}")
                print(f"📧 Email sent: {data.get('email_sent')}")
                if data.get('email_error'):
                    print(f"⚠️  Email error: {data.get('email_error')}")
                print("✅ BOOKING CREATION FIXED!")
            else:
                print("❌ Booking creation failed")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_booking_creation()