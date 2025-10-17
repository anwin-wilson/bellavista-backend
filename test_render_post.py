#!/usr/bin/env python3
"""
Test POST functionality on Render deployment
Tests the tour booking API endpoint with various scenarios
"""

import requests
import json
from datetime import datetime, timedelta

# Railway deployment URL
RAILWAY_URL = "https://bellavista-backend-production.up.railway.app"
API_BASE = f"{RAILWAY_URL}/api/tours"

def test_connection():
    """Test basic connection to the API"""
    print("🔗 Testing connection...")
    try:
        response = requests.get(f"{API_BASE}/test/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Connection successful!")
            print(f"   Status: {data.get('status')}")
            print(f"   Total bookings: {data.get('total_bookings')}")
            print(f"   DB query time: {data.get('performance', {}).get('db_query_time')}")
            return True
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_booking_endpoint_info():
    """Test GET request to booking endpoint"""
    print("\n📋 Testing booking endpoint info...")
    try:
        response = requests.get(f"{API_BASE}/book/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Booking endpoint info retrieved:")
            print(f"   Message: {data.get('message')}")
            print(f"   Methods: {data.get('methods')}")
            print(f"   Required fields: {data.get('required_fields')}")
            return True
        else:
            print(f"❌ Failed to get endpoint info: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting endpoint info: {e}")
        return False

def test_valid_booking():
    """Test creating a valid booking"""
    print("\n✅ Testing valid booking creation...")
    
    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    
    booking_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "+44 7700 900123",
        "preferred_home": "cardiff",
        "preferred_date": tomorrow.strftime("%Y-%m-%d"),
        "preferred_time": "10:00",
        "notes": "Test booking from Render deployment"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/book/",
            json=booking_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Booking created successfully!")
            print(f"   Booking ID: {data.get('booking_id')}")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Email sent: {data.get('email_sent')}")
            return data.get('booking_id')
        else:
            print(f"❌ Booking failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {error_data}")
            except:
                print(f"   Raw response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating booking: {e}")
        return None

def test_invalid_booking():
    """Test creating an invalid booking (missing required fields)"""
    print("\n❌ Testing invalid booking (missing fields)...")
    
    invalid_data = {
        "first_name": "Jane",
        # Missing required fields
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/book/",
            json=invalid_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Validation working correctly!")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Errors: {data.get('errors')}")
            return True
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid booking: {e}")
        return False

def test_available_slots():
    """Test available slots endpoint"""
    print("\n🕐 Testing available slots...")
    
    tomorrow = datetime.now() + timedelta(days=1)
    
    try:
        response = requests.get(
            f"{API_BASE}/available-slots/",
            params={
                "date": tomorrow.strftime("%Y-%m-%d"),
                "home": "cardiff"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Available slots retrieved:")
            print(f"   Date: {data.get('date')}")
            print(f"   Home: {data.get('home')}")
            print(f"   Available slots: {data.get('available_slots')}")
            return True
        else:
            print(f"❌ Failed to get available slots: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting available slots: {e}")
        return False

def test_booking_stats():
    """Test booking statistics endpoint"""
    print("\n📊 Testing booking statistics...")
    
    try:
        response = requests.get(f"{API_BASE}/stats/", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Statistics retrieved:")
            print(f"   Total bookings: {data.get('total_bookings')}")
            print(f"   Confirmed bookings: {data.get('confirmed_bookings')}")
            print(f"   Pending bookings: {data.get('pending_bookings')}")
            print(f"   Homes stats: {data.get('homes_stats')}")
            return True
        else:
            print(f"❌ Failed to get statistics: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")
        return False

def test_email_functionality():
    """Test email functionality"""
    print("\n📧 Testing email functionality...")
    
    try:
        response = requests.post(
            f"{API_BASE}/test/",
            json={"email": "test@example.com"},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            email_test = data.get('email_test', {})
            print("✅ Email test completed:")
            print(f"   Success: {email_test.get('success')}")
            print(f"   Time: {email_test.get('time')}")
            if email_test.get('error'):
                print(f"   Error: {email_test.get('error')}")
            return email_test.get('success', False)
        else:
            print(f"❌ Email test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing email: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Bellavista Backend on Railway")
    print("=" * 50)
    
    print(f"Testing URL: {RAILWAY_URL}")
    print("=" * 50)
    
    results = {}
    
    # Test connection
    results['connection'] = test_connection()
    
    if not results['connection']:
        print("\n❌ Cannot connect to API. Please check the URL and try again.")
        return
    
    # Test all endpoints
    results['endpoint_info'] = test_booking_endpoint_info()
    results['valid_booking'] = test_valid_booking() is not None
    results['invalid_booking'] = test_invalid_booking()
    results['available_slots'] = test_available_slots()
    results['booking_stats'] = test_booking_stats()
    results['email_test'] = test_email_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Railway deployment is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()