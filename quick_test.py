import requests
import time

RENDER_URL = "https://bellavista-backend-3.onrender.com"

print("🔍 Quick Render Status Check")
print("=" * 40)

# Test basic connection with longer timeout
print("Testing basic connection (30s timeout)...")
try:
    start = time.time()
    response = requests.get(f"{RENDER_URL}/", timeout=30)
    print(f"✅ Response in {time.time() - start:.1f}s - Status: {response.status_code}")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test API endpoint
print("\nTesting API endpoint...")
try:
    start = time.time()
    response = requests.get(f"{RENDER_URL}/api/tours/stats/", timeout=30)
    print(f"✅ API Response in {time.time() - start:.1f}s - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"📊 Total Bookings: {data.get('total_bookings', 0)}")
except Exception as e:
    print(f"❌ API Failed: {e}")

print("\n💡 If timeouts occur, your Render service may be 'sleeping'")
print("   Visit the URL in browser first to wake it up!")