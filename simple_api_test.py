#!/usr/bin/env python3
"""
Simple API test using only standard library
"""

import urllib.request
import urllib.parse
import json
import time
from datetime import datetime, timedelta

# Configuration
BASE_URL = "https://bellavista-backend-production.up.railway.app"  # Update with Render URL
API_BASE = f"{BASE_URL}/api/tours"

def make_request(method, endpoint, data=None, params=None):
    """Make HTTP request using urllib"""
    url = f"{API_BASE}{endpoint}"
    
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    try:
        start_time = time.time()
        
        if method == "GET":
            req = urllib.request.Request(url)
        elif method == "POST":
            json_data = json.dumps(data).encode('utf-8') if data else None
            req = urllib.request.Request(url, data=json_data)
            req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            response_time = time.time() - start_time
            content = response.read().decode('utf-8')
            
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                data = content[:200]
            
            return {
                'success': True,
                'status_code': response.getcode(),
                'response_time': f"{response_time:.3f}s",
                'data': data
            }
    
    except urllib.error.HTTPError as e:
        return {
            'success': False,
            'status_code': e.code,
            'error': f"HTTP {e.code}: {e.reason}"
        }
    except urllib.error.URLError as e:
        return {
            'success': False,
            'error': f"Connection error: {e.reason}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Error: {str(e)}"
        }

def test_api():
    """Run basic API tests"""
    print("🚀 Simple API Test for Bellavista Backend")
    print("=" * 50)
    
    # Test 1: Connection test
    print("\n1️⃣ Testing connection...")
    result = make_request("GET", "/test/")
    print(f"   Status: {'✅ PASS' if result['success'] else '❌ FAIL'}")
    if result['success']:
        print(f"   Response time: {result['response_time']}")
        print(f"   Total bookings: {result['data'].get('total_bookings', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 2: Booking info
    print("\n2️⃣ Testing booking endpoint...")
    result = make_request("GET", "/book/")
    print(f"   Status: {'✅ PASS' if result['success'] else '❌ FAIL'}")
    if result['success']:
        print(f"   Response time: {result['response_time']}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 3: Create booking
    print("\n3️⃣ Testing booking creation...")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    booking_data = {
        "first_name": "API",
        "last_name": "Test",
        "email": "apitest@example.com",
        "phone_number": "+44 7700 900456",
        "preferred_home": "cardiff",
        "preferred_date": tomorrow,
        "preferred_time": "14:00",
        "notes": "Simple API test booking"
    }
    
    result = make_request("POST", "/book/", data=booking_data)
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 201 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response time: {result['response_time']}")
        print(f"   Booking ID: {result['data'].get('booking_id', 'N/A')}")
        print(f"   Email sent: {result['data'].get('email_sent', 'N/A')}")
        if result['data'].get('email_error'):
            print(f"   Email error: {result['data']['email_error']}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 4: List bookings
    print("\n4️⃣ Testing booking list...")
    result = make_request("GET", "/bookings/")
    print(f"   Status: {'✅ PASS' if result['success'] else '❌ FAIL'}")
    if result['success']:
        print(f"   Response time: {result['response_time']}")
        bookings = result['data'].get('results', []) if isinstance(result['data'], dict) else result['data']
        print(f"   Bookings found: {len(bookings) if isinstance(bookings, list) else 'N/A'}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 5: Available slots
    print("\n5️⃣ Testing available slots...")
    params = {'date': tomorrow, 'home': 'cardiff'}
    result = make_request("GET", "/available-slots/", params=params)
    print(f"   Status: {'✅ PASS' if result['success'] else '❌ FAIL'}")
    if result['success']:
        print(f"   Response time: {result['response_time']}")
        slots = result['data'].get('available_slots', [])
        print(f"   Available slots: {slots}")
    else:
        print(f"   Error: {result['error']}")
    
    print("\n" + "=" * 50)
    print("🏁 Test complete!")

if __name__ == "__main__":
    test_api()