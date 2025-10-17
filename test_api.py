#!/usr/bin/env python3
"""
Simple API test for Render deployment
Update BASE_URL with your Render URL
"""

import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta

# Update this with your Render URL
BASE_URL = "https://your-app.onrender.com"

def test_api():
    """Test basic API functionality"""
    print("🚀 Testing Bellavista API")
    print("=" * 30)
    
    # Test connection
    try:
        url = f"{BASE_URL}/api/tours/test/"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"✅ API Status: {data['status']}")
            print(f"📊 Total Bookings: {data['total_bookings']}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    # Test booking creation
    try:
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        booking_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone_number": "+44 7700 900123",
            "preferred_home": "cardiff",
            "preferred_date": tomorrow,
            "preferred_time": "10:00",
            "notes": "API test booking"
        }
        
        url = f"{BASE_URL}/api/tours/book/"
        json_data = json.dumps(booking_data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('success'):
                print(f"✅ Booking Created: ID {data['booking_id']}")
                print(f"📧 Email Sent: {data.get('email_sent', 'N/A')}")
            else:
                print(f"❌ Booking Failed: {data.get('message', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ Booking test failed: {e}")

if __name__ == "__main__":
    test_api()