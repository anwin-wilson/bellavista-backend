#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Bellavista Backend on Render
Tests all endpoints and identifies issues for fixing
"""

import requests
import json
import time
from datetime import datetime, timedelta

# Configuration - Update this with your actual Render URL
BASE_URL = "https://bellavista-backend-production.up.railway.app"  # Railway URL (update with Render URL)
API_BASE = f"{BASE_URL}/api/tours"

def test_endpoint(method, endpoint, data=None, params=None):
    """Test a single API endpoint"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        elif method == "PATCH":
            response = requests.patch(url, json=data, timeout=30)
        
        response_time = time.time() - start_time
        
        return {
            'success': True,
            'status_code': response.status_code,
            'response_time': f"{response_time:.3f}s",
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text[:200]
        }
    
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Request timeout (30s)'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Connection error - server may be down'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': f'Request error: {str(e)}'}
    except json.JSONDecodeError:
        return {'success': False, 'error': 'Invalid JSON response'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}

def run_comprehensive_tests():
    """Run all API tests"""
    print("🚀 Starting Comprehensive API Tests for Bellavista Backend")
    print(f"📍 Testing: {BASE_URL}")
    print("=" * 60)
    
    test_results = {}
    
    # Test 1: Basic Connection Test
    print("\n1️⃣ Testing Basic Connection...")
    result = test_endpoint("GET", "/test/")
    test_results['connection_test'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        print(f"   Data: {json.dumps(result['data'], indent=2)[:200]}...")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 2: Booking Endpoint Info (GET)
    print("\n2️⃣ Testing Booking Endpoint Info...")
    result = test_endpoint("GET", "/book/")
    test_results['booking_info'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 3: Create Tour Booking (POST)
    print("\n3️⃣ Testing Tour Booking Creation...")
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
    
    result = test_endpoint("POST", "/book/", data=booking_data)
    test_results['create_booking'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 201 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        print(f"   Booking ID: {result['data'].get('booking_id', 'N/A')}")
        print(f"   Email Sent: {result['data'].get('email_sent', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 4: List All Bookings
    print("\n4️⃣ Testing Booking List...")
    result = test_endpoint("GET", "/bookings/")
    test_results['list_bookings'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        bookings = result['data'].get('results', []) if isinstance(result['data'], dict) else result['data']
        print(f"   Total Bookings: {len(bookings) if isinstance(bookings, list) else 'N/A'}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 5: Available Slots
    print("\n5️⃣ Testing Available Slots...")
    params = {
        'date': tomorrow,
        'home': 'cardiff'
    }
    result = test_endpoint("GET", "/available-slots/", params=params)
    test_results['available_slots'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        slots = result['data'].get('available_slots', [])
        print(f"   Available Slots: {slots}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 6: Booking Statistics
    print("\n6️⃣ Testing Booking Statistics...")
    result = test_endpoint("GET", "/stats/")
    test_results['booking_stats'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        stats = result['data']
        print(f"   Total Bookings: {stats.get('total_bookings', 'N/A')}")
        print(f"   Pending: {stats.get('pending_bookings', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 7: Find Nearest Home
    print("\n7️⃣ Testing Find Nearest Home...")
    params = {'location': 'Cardiff, Wales'}
    result = test_endpoint("GET", "/find-nearest-home/", params=params)
    test_results['nearest_home'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        print(f"   Nearest Home: {result['data'].get('nearest_home', 'N/A')}")
        print(f"   Distance: {result['data'].get('distance', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    # Test 8: Email Test (POST to test endpoint)
    print("\n8️⃣ Testing Email Functionality...")
    email_data = {"email": "test@example.com"}
    result = test_endpoint("POST", "/test/", data=email_data)
    test_results['email_test'] = result
    print(f"   Status: {'✅ PASS' if result['success'] and result['status_code'] == 200 else '❌ FAIL'}")
    if result['success']:
        print(f"   Response Time: {result['response_time']}")
        email_result = result['data'].get('email_test', {})
        print(f"   Email Success: {email_result.get('success', 'N/A')}")
        if not email_result.get('success'):
            print(f"   Email Error: {email_result.get('error', 'N/A')}")
    else:
        print(f"   Error: {result['error']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for result in test_results.values() if result['success'] and result.get('status_code') in [200, 201])
    total = len(test_results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    # Detailed failure analysis
    failures = []
    for test_name, result in test_results.items():
        if not result['success'] or result.get('status_code') not in [200, 201]:
            failures.append({
                'test': test_name,
                'error': result.get('error', f"HTTP {result.get('status_code', 'Unknown')}")
            })
    
    if failures:
        print("\n🔍 FAILURE ANALYSIS:")
        for failure in failures:
            print(f"   • {failure['test']}: {failure['error']}")
        
        print("\n🛠️ RECOMMENDED FIXES:")
        
        # Connection issues
        if any('Connection error' in f['error'] or 'timeout' in f['error'].lower() for f in failures):
            print("   1. Check if Render service is running and deployed")
            print("   2. Verify the BASE_URL is correct")
            print("   3. Check Render logs for startup errors")
        
        # HTTP errors
        http_errors = [f for f in failures if 'HTTP' in f['error']]
        if http_errors:
            print("   4. Check Django settings for ALLOWED_HOSTS")
            print("   5. Verify database migrations are applied")
            print("   6. Check for missing dependencies in requirements.txt")
        
        # Email errors
        if any('email' in f['test'].lower() for f in failures):
            print("   7. Configure email settings in environment variables")
            print("   8. Check SendGrid API key if using SendGrid")
    
    else:
        print("\n🎉 All tests passed! API is working correctly.")
    
    return test_results

def check_environment():
    """Check if the environment is properly configured"""
    print("\n🔧 ENVIRONMENT CHECK")
    print("=" * 30)
    
    # Test basic connectivity
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ Server reachable: {response.status_code}")
    except Exception as e:
        print(f"❌ Server unreachable: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🏥 Bellavista Care Homes - API Testing Suite")
    print("=" * 50)
    
    # Check environment first
    if not check_environment():
        print("\n❌ Environment check failed. Please verify your deployment.")
        exit(1)
    
    # Run comprehensive tests
    results = run_comprehensive_tests()
    
    # Save results to file
    with open('api_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: api_test_results.json")
    print("🏁 Testing complete!")