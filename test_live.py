#!/usr/bin/env python
"""
Live Data Test for Railway Deployment
"""

import requests
import time
from datetime import datetime

RENDER_URL = "https://bellavista-backend-3.onrender.com"

def test_endpoint(url, method="GET", data=None):
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        return {
            'success': True,
            'status_code': response.status_code,
            'response_time': time.time() - start_time,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

print("🚀 Testing Live Render Deployment")
print("=" * 50)

# Test connection
print("1. Testing Connection...")
result = test_endpoint(f"{RENDER_URL}/api/tours/test-connection/")
if result['success']:
    print(f"   ✅ Connected in {result['response_time']:.3f}s")
    if result['data']:
        print(f"   📊 Total Bookings: {result['data'].get('total_bookings', 0)}")
else:
    print(f"   ❌ Failed: {result['error']}")

# Test stats
print("\n2. Getting Live Stats...")
result = test_endpoint(f"{RENDER_URL}/api/tours/stats/")
if result['success'] and result['data']:
    stats = result['data']
    print(f"   📈 Total: {stats.get('total_bookings', 0)}")
    print(f"   ✅ Confirmed: {stats.get('confirmed_bookings', 0)}")
    print(f"   ⏳ Pending: {stats.get('pending_bookings', 0)}")
    print(f"   ⏱️  Response: {result['response_time']:.3f}s")

# Create test booking
print("\n3. Creating Test Booking...")
test_booking = {
    'first_name': 'Live',
    'last_name': 'Test',
    'email': 'livetest@bellavista.com',
    'phone_number': '07999888777',
    'preferred_home': 'cardiff',
    'preferred_date': '2024-12-25',
    'preferred_time': '15:00',
    'notes': f'Live test - {datetime.now().strftime("%H:%M:%S")}'
}

result = test_endpoint(f"{RENDER_URL}/api/tours/book/", "POST", test_booking)
if result['success']:
    print(f"   ✅ Booking created in {result['response_time']:.3f}s")
    if result['data']:
        print(f"   🆔 ID: {result['data'].get('booking_id')}")
        print(f"   📧 Email: {result['data'].get('email_sent')}")
else:
    print(f"   ❌ Failed: {result.get('error')}")

print(f"\n✨ Live testing completed!")
print(f"🌐 Render URL: {RENDER_URL}")