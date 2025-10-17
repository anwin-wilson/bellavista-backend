#!/usr/bin/env python
"""
Performance Test Script for Bellavista Care Homes API
Tests API response times and identifies bottlenecks
"""

import requests
import time
import json
from datetime import datetime

# Configuration
RAILWAY_URL = "https://bellavista-backend-production.up.railway.app"
LOCAL_URL = "http://127.0.0.1:8000"

def test_endpoint(url, method="GET", data=None, timeout=10):
    """Test a single endpoint and measure response time"""
    try:
        start_time = time.time()
        
        if method == "GET":
            response = requests.get(url, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return {
            'success': True,
            'status_code': response.status_code,
            'response_time': response_time,
            'size': len(response.content),
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'response_time': time.time() - start_time
        }

def run_performance_tests(base_url):
    """Run comprehensive performance tests"""
    
    print(f"🚀 Testing API Performance: {base_url}")
    print("=" * 60)
    
    tests = [
        {
            'name': 'Connection Test',
            'url': f"{base_url}/api/tours/test-connection/",
            'method': 'GET'
        },
        {
            'name': 'Booking Stats',
            'url': f"{base_url}/api/tours/stats/",
            'method': 'GET'
        },
        {
            'name': 'Available Slots',
            'url': f"{base_url}/api/tours/available-slots/?date=2024-01-15&home=cardiff",
            'method': 'GET'
        },
        {
            'name': 'List Bookings',
            'url': f"{base_url}/api/tours/bookings/",
            'method': 'GET'
        },
        {
            'name': 'Create Booking',
            'url': f"{base_url}/api/tours/book/",
            'method': 'POST',
            'data': {
                'first_name': 'Performance',
                'last_name': 'Test',
                'email': 'test@example.com',
                'phone_number': '07123456789',
                'preferred_home': 'cardiff',
                'preferred_date': '2024-01-15',
                'preferred_time': '14:00',
                'notes': 'Performance test booking'
            }
        }
    ]
    
    results = []
    total_time = 0
    
    for test in tests:
        print(f"Testing: {test['name']}...")
        
        result = test_endpoint(
            test['url'], 
            test.get('method', 'GET'), 
            test.get('data')
        )
        
        result['name'] = test['name']
        results.append(result)
        
        if result['success']:
            print(f"  ✅ {result['response_time']:.3f}s - Status: {result['status_code']}")
            total_time += result['response_time']
        else:
            print(f"  ❌ Failed: {result['error']}")
        
        time.sleep(0.5)  # Small delay between requests
    
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    
    successful_tests = [r for r in results if r['success']]
    
    if successful_tests:
        avg_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
        fastest = min(successful_tests, key=lambda x: x['response_time'])
        slowest = max(successful_tests, key=lambda x: x['response_time'])
        
        print(f"Total Tests: {len(results)}")
        print(f"Successful: {len(successful_tests)}")
        print(f"Failed: {len(results) - len(successful_tests)}")
        print(f"Average Response Time: {avg_time:.3f}s")
        print(f"Fastest: {fastest['name']} ({fastest['response_time']:.3f}s)")
        print(f"Slowest: {slowest['name']} ({slowest['response_time']:.3f}s)")
        
        # Performance recommendations
        print("\n🎯 PERFORMANCE RECOMMENDATIONS:")
        if avg_time > 2.0:
            print("  ⚠️  Average response time is high (>2s)")
            print("     - Consider database optimization")
            print("     - Add caching for frequently accessed data")
        elif avg_time > 1.0:
            print("  ⚡ Response times are acceptable but could be improved")
            print("     - Consider adding database indexes")
        else:
            print("  ✅ Response times are good (<1s average)")
        
        # Check for specific slow endpoints
        slow_endpoints = [r for r in successful_tests if r['response_time'] > 3.0]
        if slow_endpoints:
            print(f"\n  🐌 Slow endpoints (>3s):")
            for endpoint in slow_endpoints:
                print(f"     - {endpoint['name']}: {endpoint['response_time']:.3f}s")
    
    return results

def test_email_performance(base_url):
    """Test email functionality performance"""
    print("\n📧 TESTING EMAIL PERFORMANCE")
    print("=" * 60)
    
    test_email = input("Enter email for testing (or press Enter to skip): ").strip()
    if not test_email:
        print("Skipping email test...")
        return
    
    print("Testing email functionality...")
    result = test_endpoint(
        f"{base_url}/api/tours/test-connection/",
        method="POST",
        data={'email': test_email},
        timeout=30  # Email might take longer
    )
    
    if result['success']:
        print(f"✅ Email test completed in {result['response_time']:.3f}s")
        if result['data'] and 'email_test' in result['data']:
            email_result = result['data']['email_test']
            if email_result['success']:
                print(f"   📧 Email sent successfully to {email_result['sent_to']}")
                print(f"   ⏱️  Email sending time: {email_result['time']}")
            else:
                print(f"   ❌ Email failed: {email_result['error']}")
    else:
        print(f"❌ Email test failed: {result['error']}")

if __name__ == "__main__":
    print("🔍 Bellavista Care Homes - API Performance Test")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test production URL
    print("\n" + "🌐 TESTING PRODUCTION API")
    production_results = run_performance_tests(BASE_URL)
    
    # Test email performance
    test_email_performance(BASE_URL)
    
    print(f"\n✨ Performance testing completed!")
    print(f"Results saved with timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")