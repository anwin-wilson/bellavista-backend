import requests
import time

# Both deployment URLs
RENDER_URL = "https://bellavista-backend-3.onrender.com"
RAILWAY_URL = "https://bellavista-backend-production.up.railway.app"

def test_deployment(name, base_url):
    print(f"\n🚀 TESTING {name}")
    print("=" * 50)
    
    # Test basic connection
    try:
        response = requests.get(f"{base_url}/api/tours/stats/", timeout=30)
        print(f"✅ Connection: {response.status_code} ({time.time():.1f}s)")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Total Bookings: {data.get('total_bookings', 0)}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    # Test POST - Create booking
    booking_data = {
        'first_name': 'API',
        'last_name': 'Test',
        'email': 'test@example.com',
        'phone_number': '07123456789',
        'preferred_home': 'cardiff',
        'preferred_date': '2024-12-25',
        'preferred_time': '15:00',
        'notes': f'{name} test booking'
    }
    
    try:
        start = time.time()
        response = requests.post(f"{base_url}/api/tours/book/", json=booking_data, timeout=30)
        elapsed = time.time() - start
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ POST Booking: Created in {elapsed:.2f}s")
            print(f"   ID: {data.get('booking_id')}")
            print(f"   Email Sent: {data.get('email_sent')}")
        else:
            print(f"❌ POST Booking: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"❌ POST Booking failed: {e}")
    
    # Test email endpoint
    try:
        response = requests.get(f"{base_url}/api/tours/test/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Email Config: {data.get('email_configured', False)}")
        else:
            print(f"❌ Email endpoint: {response.status_code}")
    except Exception as e:
        print(f"❌ Email test failed: {e}")
    
    return True

# Test both deployments
print("🔍 COMPARING DEPLOYMENTS")
print("Testing POST functionality and email on both platforms")

# Test Render
render_works = test_deployment("RENDER", RENDER_URL)

# Test Railway  
railway_works = test_deployment("RAILWAY", RAILWAY_URL)

# Summary
print(f"\n📋 SUMMARY")
print("=" * 30)
print(f"Render:  {'✅ Working' if render_works else '❌ Failed'}")
print(f"Railway: {'✅ Working' if railway_works else '❌ Failed'}")

if render_works and railway_works:
    print("\n💡 Both deployments working!")
elif render_works:
    print("\n💡 Use Render deployment")
elif railway_works:
    print("\n💡 Use Railway deployment")
else:
    print("\n⚠️  Both deployments have issues")